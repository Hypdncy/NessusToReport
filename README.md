# NessusToReport
这是一个nessus自动报告生成工具，可以用来自动生成nessus扫描器的中文报告--NessusToReport,

GitHub:`https://github.com/Hypdncy/NessusToReport`

*版权所有，侵权必究*

*本项目，仅仅代表个人，如有侵权，请通知我删除*

## 配置

1. config.py：用户配置信息的位置  

    1. data.date:配置时间,参见default
    1. data.monitor:配置监督者,参见default
    1. data.manager:配置管理者,参见default
    1. data.work:配置工作者,参见default
    1. datasystems:配置IP和系统的关系，该项错误可能导致报错
    1. ignores:报告生成过程中忽略的nessusid
    1. nessus_vuln_self:自定义的漏洞信息

    *若漏洞不存在数据库中，可以通过配置自定义nessus_vuln_self来添加*
        
1. cnf/default.py:默认的信息配置，该部分的信息会更新到data中，默认信息
1. cnf/data.py：全局信息

变量覆盖顺序：config.py > default.py > data.py

## 使用

1. 导入nessus的csv，放置到csv/nessus/目录下
1. 更新属于自己的模板文档并放置在template目录下
    
    1. 将modle/docx_draw_host.py中"公司信息"替换为"$自己的公司"
    
1. 配置default.py、config.py为自己的信息
1. 执行命令

```shell script
python main.py -t host # 指定扫描报告类型
python main.py # 默认主机扫描报告
```

> 配置出错

出错的时候一般都是漏洞信息不再数据库中也不在config.py中，这时不存在的漏洞信息将会自动dump到errors.json中,

可以翻译该文件中的字符串，并将其更新到config.py的nessus_vuln_self中

## 更新

1. 项目不定期发布漏洞库vuln.db，在release中可以下载，并替换到./cnf/目录下
2. 各位可以将errors.json中的信息写到到updatedb.txt中，并且push到github，我将会翻译并将其更新其到数据库中

## 演示图

![演示图](演示图.jpg)

## 特别谢鸣

