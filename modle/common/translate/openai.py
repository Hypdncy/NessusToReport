#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ------------------------------------------------------------
# File: openai.py
# Created Date: 2026/06/02
# ------------------------------------------------------------

import asyncio
import json
import logging
import re
from aiohttp import ClientResponse
from modle.common.loophole.loopholes import Loopholes
from modle.common.translate.base import TranBase


class TranOpenAI(TranBase):

    def __init__(self, LOOPHOLES: Loopholes):
        super(TranOpenAI, self).__init__(LOOPHOLES)
        from cnf.const import translate_openai_key, translate_openai_model
        self.api_key = translate_openai_key
        self.model = translate_openai_model

    def _make_en_reqinfos(self):
        en_reqinfos = []
        for plugin_id in self.LOOPHOLES:
            if self.LOOPHOLES[plugin_id]["describe_cn"]:
                continue
            self.tran_count += 1
            en_reqinfos.append({
                "type_cn": "all",
                "plugin_id": plugin_id,
                "name_en": self.LOOPHOLES[plugin_id]["name_en"],
                "describe_en": self.LOOPHOLES[plugin_id]["describe_en"],
                "solution_en": self.LOOPHOLES[plugin_id]["solution_en"],
            })
        return en_reqinfos

    async def _analysis_cn_resinfo(self, response: ClientResponse, type_cn):
        pass

    def _parse_json_response(self, text):
        text = text.strip()
        text = re.sub(r'^```json\s*', '', text)
        text = re.sub(r'^```\s*', '', text)
        text = re.sub(r'\s*```$', '', text)
        text = text.strip()
        return json.loads(text)

    async def _tran_http(self, reqinfo, sem=None):
        from openai import AsyncOpenAI
        from cnf.const import translate_openai_base_url
        client = AsyncOpenAI(api_key=self.api_key, base_url=translate_openai_base_url)

        prompt = f"""请将以下Nessus漏洞信息翻译成中文，只返回JSON格式，不要有其他内容：
{{
    "name_cn": "漏洞名称中文",
    "describe_cn": "漏洞描述中文",
    "solution_cn": "解决方案中文"
}}

英文信息:
- 名称: {reqinfo['name_en']}
- 描述: {reqinfo['describe_en']}
- 解决方案: {reqinfo['solution_en']}"""

        for attempt in range(3):
            try:
                response = await client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": "你是一个专业的网络安全漏洞翻译专家。请将Nessus漏洞的英文名称、描述和解决方案翻译成准确的中文，只返回JSON格式的翻译结果。"},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.3,
                    max_tokens=1000
                )

                result_text = response.choices[0].message.content.strip()
                data = self._parse_json_response(result_text)

                self.tran_number += 1
                print("------翻译漏洞进度：{0}/{1}".format(self.tran_number, self.tran_count), end='\r')
                return [reqinfo["plugin_id"], data]
            except json.JSONDecodeError as e:
                if attempt < 2:
                    logging.warning("------JSON解析失败，重试中：plugin_id={}, error={}".format(reqinfo["plugin_id"], e))
                    await asyncio.sleep(1)
                    continue
                logging.error("------翻译失败JSON解析错误：plugin_id={}".format(reqinfo["plugin_id"]))
                logging.error(e)
                return [0, {}]
            except Exception as e:
                logging.error("------翻译失败：plugin_id={}".format(reqinfo["plugin_id"]))
                logging.error(e)
                return [0, {}]

    async def _tran_http_with_sem(self, reqinfo, sem):
        async with sem:
            return await self._tran_http(reqinfo, sem)