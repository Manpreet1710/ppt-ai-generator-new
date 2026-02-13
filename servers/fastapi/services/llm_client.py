import asyncio
import dirtyjson
import json
import logging
from typing import AsyncGenerator, List, Optional
from fastapi import HTTPException
from google import genai
from google.genai.types import Content as GoogleContent, Part as GoogleContentPart
from google.genai.types import (
    GenerateContentConfig,
    GoogleSearch,
    ToolConfig as GoogleToolConfig,
    FunctionCallingConfig as GoogleFunctionCallingConfig,
    FunctionCallingConfigMode as GoogleFunctionCallingConfigMode,
)
from google.genai.types import Tool as GoogleTool
from enums.llm_provider import LLMProvider
from models.llm_message import (
    GoogleAssistantMessage,
    GoogleToolCallMessage,
    LLMMessage,
    LLMSystemMessage,
    LLMUserMessage,
)
from models.llm_tool_call import (GoogleToolCall)
from models.llm_tools import LLMDynamicTool, LLMTool
from services.llm_tool_calls_handler import LLMToolCallsHandler
from utils.async_iterator import iterator_to_async
from utils.get_env import (
    get_disable_thinking_env,
    get_google_api_key_env,
    get_tool_calls_env,
    get_web_grounding_env,
)
from utils.llm_provider import get_llm_provider, get_model
from utils.parsers import parse_bool_or_none
from utils.schema_utils import (
    flatten_json_schema,
    remove_titles_from_schema,
)

logger = logging.getLogger(__name__)

class LLMClient:
    def __init__(self):
        self.llm_provider = get_llm_provider()
        self._client = self._get_client()
        self.tool_calls_handler = LLMToolCallsHandler(self)

    # ? Use tool calls
    def use_tool_calls_for_structured_output(self) -> bool:
        if self.llm_provider != LLMProvider.CUSTOM:
            return False
        return parse_bool_or_none(get_tool_calls_env()) or False

    # ? Web Grounding
    def enable_web_grounding(self) -> bool:
        if (
            self.llm_provider == LLMProvider.OLLAMA
            or self.llm_provider == LLMProvider.CUSTOM
        ):
            return False
        return parse_bool_or_none(get_web_grounding_env()) or False

    # ? Disable thinking
    def disable_thinking(self) -> bool:
        return parse_bool_or_none(get_disable_thinking_env()) or False

    # ? Clients
    def _get_client(self):
        match self.llm_provider:
            case LLMProvider.OPENAI:
                return self._get_openai_client()
            case LLMProvider.GOOGLE:
                return self._get_google_client()
            case LLMProvider.ANTHROPIC:
                return self._get_anthropic_client()
            case LLMProvider.OLLAMA:
                return self._get_ollama_client()
            case LLMProvider.CUSTOM:
                return self._get_custom_client()
            case _:
                raise HTTPException(
                    status_code=400,
                    detail="LLM Provider must be either openai, google, anthropic, ollama, or custom",
                )

    def _get_google_client(self):
        if not get_google_api_key_env():
            raise HTTPException(
                status_code=400,
                detail="Google API Key is not set",
            )
        return genai.Client()

   
    # ? Prompts
    def _get_system_prompt(self, messages: List[LLMMessage]) -> str:
        for message in messages:
            if isinstance(message, LLMSystemMessage):
                return message.content
        return ""

    def _get_google_messages(self, messages: List[LLMMessage]) -> List[GoogleContent]:
        contents = []
        for message in messages:
            if isinstance(message, LLMUserMessage):
                contents.append(
                    GoogleContent(
                        role=message.role,
                        parts=[GoogleContentPart(text=message.content)],
                    )
                )
            elif isinstance(message, GoogleAssistantMessage):
                contents.append(message.content)
            elif isinstance(message, GoogleToolCallMessage):
                contents.append(
                    GoogleContent(
                        role="user",
                        parts=[
                            GoogleContentPart.from_function_response(
                                name=message.name,
                                response=message.response,
                            )
                        ],
                    )
                )

        return contents

    
    # //LLM Calls

    async def generate(
        self,
        model: str,
        messages: List[LLMMessage],
        max_tokens: Optional[int] = None,
        tools: Optional[List[type[LLMTool] | LLMDynamicTool]] = None,
    ):
        parsed_tools = self.tool_calls_handler.parse_tools(tools)
        content = None
        match self.llm_provider:
            case LLMProvider.GOOGLE:
                content = await self._generate_google(
                    model=model,
                    messages=messages,
                    max_tokens=max_tokens,
                    tools=parsed_tools,
                )
        if content is None:
            raise HTTPException(
                status_code=400,
                detail="LLM did not return any content",
            )
        return content

    async def _generate_google(
        self,
        model: str,
        messages: List[LLMMessage],
        tools: Optional[List[dict]] = None,
        max_tokens: Optional[int] = None,
        depth: int = 0,
    ) -> str | None:
        client: genai.Client = self._client

        google_tools = None
        if tools:
            google_tools = [GoogleTool(function_declarations=[tool]) for tool in tools]

        response = await asyncio.to_thread(
            client.models.generate_content,
            model=model,
            contents=self._get_google_messages(messages),
            config=GenerateContentConfig(
                tools=google_tools,
                system_instruction=self._get_system_prompt(messages),
                response_mime_type="text/plain",
                max_output_tokens=max_tokens,
            ),
        )
        content = response.candidates[0].content
        response_parts = content.parts

        usage = response.usage_metadata
        if usage:
            logger.info(
                f"[Gemini Usage] input={usage.prompt_token_count} | output={usage.candidates_token_count} | total={usage.total_token_count}"
            )

        if not response_parts:
            return None

        text_content = None
        tool_calls = []
        for each_part in response_parts:
            if each_part.function_call:
                tool_calls.append(
                    GoogleToolCall(
                        id=each_part.function_call.id,
                        name=each_part.function_call.name,
                        arguments=each_part.function_call.args,
                    )
                )
            if each_part.text:
                text_content = each_part.text

        if tool_calls:
            tool_call_messages = await self.tool_calls_handler.handle_tool_calls_google(
                tool_calls
            )
            new_messages = [
                *messages,
                GoogleAssistantMessage(
                    role="assistant",
                    content=content,
                ),
                *tool_call_messages,
            ]
            return await self._generate_google(
                model=model,
                messages=new_messages,
                max_tokens=max_tokens,
                tools=tools,
                depth=depth + 1,
            )

        return text_content
   
    def stream(
        self,
        model: str,
        messages: List[LLMMessage],
        max_tokens: Optional[int] = None,
        tools: Optional[List[type[LLMTool] | LLMDynamicTool]] = None,
    ):
        parsed_tools = self.tool_calls_handler.parse_tools(tools)
        match self.llm_provider:
            case LLMProvider.GOOGLE:
                return self._stream_google(
                    model=model,
                    messages=messages,
                    max_tokens=max_tokens,
                    tools=parsed_tools,
                )
    
    async def _stream_google(
        self,
        model: str,
        messages: List[LLMMessage],
        tools: Optional[List[dict]] = None,
        max_tokens: Optional[int] = None,
        depth: int = 0,
    ) -> AsyncGenerator[str, None]:
        client: genai.Client = self._client

        google_tools = None
        if tools:
            google_tools = [GoogleTool(function_declarations=[tool]) for tool in tools]

        generated_contents = []
        tool_calls: List[GoogleToolCall] = []
        usage = None
        async for event in iterator_to_async(client.models.generate_content_stream)(
            model=model,
            contents=self._get_google_messages(messages),
            config=GenerateContentConfig(
                system_instruction=self._get_system_prompt(messages),
                response_mime_type="text/plain",
                tools=google_tools,
                max_output_tokens=max_tokens,
            ),
        ):
            if hasattr(event, "usage_metadata") and event.usage_metadata:
                usage = event.usage_metadata

            if not (
                event.candidates
                and event.candidates[0].content
                and event.candidates[0].content.parts
            ):
                continue

            generated_contents.append(event.candidates[0].content)

            for each_part in event.candidates[0].content.parts:
                if each_part.text:
                    yield each_part.text

                if each_part.function_call:
                    tool_calls.append(
                        GoogleToolCall(
                            id=each_part.function_call.id,
                            name=each_part.function_call.name,
                            arguments=each_part.function_call.args,
                        )
                    )

        if usage:
            logger.info(
                f"[Gemini Usage] input={usage.prompt_token_count} | output={usage.candidates_token_count} | total={usage.total_token_count}"
            )

        if tool_calls:
            tool_call_messages = await self.tool_calls_handler.handle_tool_calls_google(
                tool_calls
            )
            new_messages = [
                *messages,
                *[
                    GoogleAssistantMessage(
                        role="assistant",
                        content=each,
                    )
                    for each in generated_contents
                ],
                *tool_call_messages,
            ]
            async for event in self._stream_google(
                model=model,
                messages=new_messages,
                max_tokens=max_tokens,
                tools=tools,
                depth=depth + 1,
            ):
                yield event




    async def generate_structured(
        self,
        model: str,
        messages: List[LLMMessage],
        response_format: dict,
        strict: bool = False,
        tools: Optional[List[type[LLMTool] | LLMDynamicTool]] = None,
        max_tokens: Optional[int] = None,
    ) -> dict:
        parsed_tools = self.tool_calls_handler.parse_tools(tools)
        content = None
        match self.llm_provider:
            case LLMProvider.GOOGLE:
                content = await self._generate_google_structured(
                    model=model,
                    messages=messages,
                    response_format=response_format,
                    tools=parsed_tools,
                    max_tokens=max_tokens,
                )
        if content is None:
            raise HTTPException(
                status_code=400,
                detail="LLM did not return any content",
            )
        return content

    async def _generate_google_structured(
        self,
        model: str,
        messages: List[LLMMessage],
        response_format: dict,
        max_tokens: Optional[int] = None,
        tools: Optional[List[dict]] = None,
        depth: int = 0,
    ) -> dict | None:
        client: genai.Client = self._client

        google_tools = None
        if tools:
            google_tools = [GoogleTool(function_declarations=[tool]) for tool in tools]
            google_tools.append(
                GoogleTool(
                    function_declarations=[
                        {
                            "name": "ResponseSchema",
                            "description": "Provide response to the user",
                            "parameters": remove_titles_from_schema(
                                flatten_json_schema(response_format)
                            ),
                        }
                    ]
                )
            )
        response = await asyncio.to_thread(
            client.models.generate_content,
            model=model,
            contents=self._get_google_messages(messages),
            config=GenerateContentConfig(
                tools=google_tools,
                tool_config=(
                    GoogleToolConfig(
                        function_calling_config=GoogleFunctionCallingConfig(
                            mode=GoogleFunctionCallingConfigMode.ANY,
                        ),
                    )
                    if tools
                    else None
                ),
                system_instruction=self._get_system_prompt(messages),
                response_mime_type="application/json" if not tools else None,
                response_json_schema=response_format if not tools else None,
                max_output_tokens=max_tokens,
            ),
        )

        content = response.candidates[0].content
        response_parts = content.parts
        text_content = None

        # Log usage with detailed breakdown
        usage = response.usage_metadata
        if usage:
            print(f"[Gemini Usage]")
            print(f"  Input Tokens:  {usage.prompt_token_count:,}")
            print(f"  Output Tokens: {usage.candidates_token_count:,}")
            print(f"  Total Tokens:  {usage.total_token_count:,}")

        if not response_parts:
            print(f"[Warning] No response parts received at depth {depth}")
            return None

        tool_calls: List[GoogleToolCall] = []
        for each_part in response_parts:
            if each_part.function_call:
                tool_calls.append(
                    GoogleToolCall(
                        id=each_part.function_call.id,
                        name=each_part.function_call.name,
                        arguments=each_part.function_call.args,
                    )
                )

            if each_part.text:
                text_content = each_part.text

        # Log response content
        if tool_calls:
            # print(f"[Tool Calls Received - Depth {depth}]: {len(tool_calls)}")
            for tc in tool_calls:
                print(f"  - {tc.name}")
        if text_content:
            text_preview = text_content[:200] + "..." if len(text_content) > 200 else text_content
            # print(f"[Text Content - Depth {depth}]: {text_preview}\n")

        for each in tool_calls:
            if each.name == "ResponseSchema":
                # print(f"[ResponseSchema Found - Depth {depth}] Returning structured response\n")
                return each.arguments

        if tool_calls:
            # print(f"[Executing Tool Calls - Depth {depth}] Recursing with new messages...\n")
            tool_call_messages = await self.tool_calls_handler.handle_tool_calls_google(
                tool_calls
            )
            new_messages = [
                *messages,
                GoogleAssistantMessage(
                    role="assistant",
                    content=content,
                ),
                *tool_call_messages,
            ]
            return await self._generate_google_structured(
                model=model,
                messages=new_messages,
                max_tokens=max_tokens,
                response_format=response_format,
                tools=tools,
                depth=depth + 1,
            )

        if text_content:
            # print(f"[Parsing JSON - Depth {depth}] Converting text to dict\n")
            return dict(dirtyjson.loads(text_content))
        
        # print(f"[Warning] No valid response at depth {depth}\n")
        return None
   


    #used for generate outline
    
    def stream_structured(
        self,
        model: str,
        messages: List[LLMMessage],
        response_format: dict,
        strict: bool = False,
        tools: Optional[List[type[LLMTool] | LLMDynamicTool]] = None,
        max_tokens: Optional[int] = None,
    ):
        parsed_tools = self.tool_calls_handler.parse_tools(tools)
        match self.llm_provider:
            case LLMProvider.GOOGLE:
                return self._stream_google_structured(
                    model=model,
                    messages=messages,
                    response_format=response_format,
                    tools=parsed_tools,
                    max_tokens=max_tokens,
                )

    async def _stream_google_structured(
        self,
        model: str,
        messages: List[LLMMessage],
        response_format: dict,
        max_tokens: Optional[int] = None,
        tools: Optional[List[dict]] = None,
        depth: int = 0,
    ) -> AsyncGenerator[str, None]:

        client: genai.Client = self._client

        google_tools = None
        if tools:
            google_tools = [GoogleTool(function_declarations=[tool]) for tool in tools]
            google_tools.append(
                GoogleTool(
                    function_declarations=[
                        {
                            "name": "ResponseSchema",
                            "description": "Provide response to the user",
                            "parameters": remove_titles_from_schema(
                                flatten_json_schema(response_format)
                            ),
                        }
                    ]
                )
            )

        parsed_messages = self._get_google_messages(messages)

        generated_contents = []
        tool_calls: List[GoogleToolCall] = []
        has_response_schema_tool_call = False
        usage = None
        all_events = []  # Store all events
        
        async for event in iterator_to_async(client.models.generate_content_stream)(
            model=model,
            contents=parsed_messages,
            config=GenerateContentConfig(
                tools=google_tools,
                tool_config=(
                    GoogleToolConfig(
                        function_calling_config=GoogleFunctionCallingConfig(
                            mode=GoogleFunctionCallingConfigMode.ANY,
                        ),
                    )
                    if tools
                    else None
                ),
                system_instruction=self._get_system_prompt(messages),
                response_mime_type="application/json" if not tools else None,
                response_json_schema=response_format if not tools else None,
                max_output_tokens=max_tokens,
            ),
        ):
            if hasattr(event, "usage_metadata") and event.usage_metadata:
                usage = event.usage_metadata
            
            if not (
                event.candidates
                and event.candidates[0].content
                and event.candidates[0].content.parts
            ):
                continue

            generated_contents.append(event.candidates[0].content)
            all_events.append(event)  # Store each event

        # Log usage after stream completes
        if usage:
            # logger.info(f"[Gemini Usage] input={usage.prompt_token_count} | output={usage.candidates_token_count} | total={usage.total_token_count}")
            print(f"[Gemini Usage] input={usage.prompt_token_count} | output={usage.candidates_token_count} | total={usage.total_token_count}")

        # Process all events to collect text and tool calls
        for event in all_events:
            if not (event.candidates and event.candidates[0].content and event.candidates[0].content.parts):
                continue
                
            for each_part in event.candidates[0].content.parts:
                if each_part.text and not google_tools:
                    yield each_part.text

                if each_part.function_call:
                    if each_part.function_call.name == "ResponseSchema":
                        has_response_schema_tool_call = True
                        if each_part.function_call.args:
                            yield json.dumps(each_part.function_call.args)

                    tool_calls.append(
                        GoogleToolCall(
                            id=each_part.function_call.id,
                            name=each_part.function_call.name,
                            arguments=each_part.function_call.args,
                        )
                    )

        if tool_calls and not has_response_schema_tool_call:
            tool_call_messages = await self.tool_calls_handler.handle_tool_calls_google(
                tool_calls
            )
            new_messages = [
                *messages,
                *[
                    GoogleAssistantMessage(
                        role="assistant",
                        content=each,
                    )
                    for each in generated_contents
                ],
                *tool_call_messages,
            ]
            async for event in self._stream_google_structured(
                model=model,
                messages=new_messages,
                max_tokens=max_tokens,
                response_format=response_format,
                tools=tools,
                depth=depth + 1,
            ):
                yield event
    
    
    async def _search_google(self, query: str) -> str:
        client: genai.Client = self._client
        grounding_tool = GoogleTool(google_search=GoogleSearch())
        config = GenerateContentConfig(tools=[grounding_tool])

        response = await asyncio.to_thread(
            client.models.generate_content,
            model=get_model(),
            contents=query,
            config=config,
        )
        return response.text