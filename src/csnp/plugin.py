#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File     :   plugin.py
@Time     :   2023/09/14 16:31:00
@Author   :   zhouwei
@Email    :   zhouwei@linux.com
@Function :   main file
'''
import json
import requests
from django import forms
from sentry.plugins.bases.notify import NotificationPlugin
import csnp


# 钉钉及微信的基础url
wechat_webhook = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key="
dingtalk_webhook = "https://oapi.dingtalk.com/robot/send?access_token="


# 基于django的页面表单
class CrewForm(forms.Form):
    '''token的表单'''
    key = forms.CharField(
        max_length=255, help_text='企业微信机器人的key', required=False)
    access_token = forms.CharField(
        max_length=255, help_text='钉钉机器人的access_token', required=False)


class CrewPlugin(NotificationPlugin):
    '''机组通知插件'''
    author = 'zhouwei'
    author_url = 'https://github.com/xiaomao361/csnp'
    version = csnp.VERSION
    description = "机组发送错误消息的插件，目前包含企业微信及钉钉"
    resource_links = [
        ('Bug Tracker', 'https://github.com/xiaomao361/csnp/issues'),
        ('Source', 'https://github.com/xiaomao361/csnp'),
    ]
    slug = 'crew member notification'
    title = 'crew member notification'
    conf_key = slug
    conf_title = title
    project_conf_form = CrewForm

    def is_configured(self, project):
        '''检查是否配置'''
        urls = []
        if self.get_option('key', project):
            urls.append(wechat_webhook + self.get_option('key', project))
        if self.get_option('access_token', project):
            urls.append(dingtalk_webhook +
                        self.get_option('access_token', project))
        return urls

    def notify_users(self, group, event, *args, **kwargs):
        '''通知用户'''
        urls = self.is_configured(group.project)

        if len(urls) == 0:
            self.logger.info('wechat key or dingtalk token config error')
            return None
        if self.should_notify(group, event):
            self.logger.info('now send msg to crew member')
            for url in urls:
                self.send_msg(group, event, url, *args, **kwargs)
                return 'success'
        else:
            self.logger.info('no need send msg to crew member')
            return None

    def send_msg(self, group, event, url, *args, **kwargs):
        '''发送消息'''
        del args, kwargs
        error_title = f"项目【{event.project.slug}】报错"
        base_url = group.get_absolute_url()
        event_id = event.event_id if hasattr(event, 'event_id') else event.id
        check_url = base_url + 'events/' + event_id
        data = {}
        if 'weixin' in url:
            data = {
                "msgtype": 'markdown',
                "markdown": {
                    "content": f"#### {error_title} \n\n > {event.message} \n\n [点击查看问题]({check_url})"
                }
            }
        if 'dingtalk' in url:
            data = {
                "msgtype": 'markdown',
                "markdown": {
                    "title": error_title,
                    "text": f"#### {error_title} \n\n > {event.message} \n\n [点击查看问题]({check_url})"
                }
            }
        requests.post(url=url,
                      headers={'Content-Type': 'application/json'},
                      data=json.dumps(data).encode('utf-8'),
                      timeout=10)
