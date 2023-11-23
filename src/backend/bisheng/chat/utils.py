from bisheng.api.v1.schemas import ChatMessage
from bisheng.interface.utils import try_setting_streaming_options
from bisheng.processing.base import get_result_and_steps
from bisheng.utils.logger import logger
from bisheng_langchain.chat_models import HostQwenChat
from fastapi import WebSocket
from langchain import LLMChain, PromptTemplate
from langchain.chat_models import ChatOpenAI

async def process_graph(
    langchain_object,
    chat_inputs: ChatMessage,
    websocket: WebSocket,
):
    langchain_object = try_setting_streaming_options(langchain_object, websocket)
    logger.debug('Loaded langchain object')

    if langchain_object is None:
        # Raise user facing error
        raise ValueError(
            'There was an error loading the langchain_object. Please, check all the nodes and try again.'
        )

    # Generate result and thought
    try:
        if not chat_inputs.message:
            logger.debug('No message provided')
            raise ValueError('No message provided')

        logger.debug('Generating result and thought')
        result, intermediate_steps, source_document = await get_result_and_steps(
            langchain_object, chat_inputs.message, websocket=websocket)
        logger.debug('Generated result and intermediate_steps')
        return result, intermediate_steps, source_document
    except Exception as e:
        # Log stack trace
        logger.exception(e)
        raise e


prompt_template = '''You will be provided with a block of text, and your task is to extract a list of keywords from it, and output them in a list format

Examples:
Question: The current ratio of Dameng Company in the past three years is as follows: 2021: 3.74 times; 2020: 2.82 times; 2019: 2.05 times. 
KeyWords: ['past three years', 'current ratio', '2021', '3.74', '2020', '2.82', '2019', '2.05']

----------------
Question: {question}'''


def extract_answer_keys(answer, extract_model, host_base_url):
    """
    提取answer中的关键词
    """
    if extract_model:
        # llm = HostQwenChat(model_name=extract_model,
        #                    host_base_url=host_base_url,
        #                    max_tokens=8192,
        #                    temperature=0,
        #                    verbose=True)
        llm = ChatOpenAI(
            streaming=False,
            openai_api_key=host_base_url['api_key'],
            openai_api_base=host_base_url['api_base'],
            model_name=extract_model,
            temperature=0
            )

        llm_chain = LLMChain(llm=llm, prompt=PromptTemplate.from_template(prompt_template))
    try:
        keywords_str = llm_chain.run(answer)
        keywords = eval(keywords_str[9:])
    except Exception:
        import jieba.analyse
        logger.warning(f'llm {extract_model} extract_not_support, change to jieba')
        keywords = jieba.analyse.extract_tags(answer, topK=100, withWeight=False)

    return keywords
