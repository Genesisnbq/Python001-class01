# SQL TO PANDAS - 倪彬琪

| 序号 | 操作       | SQL       | Pandas        |
|-------|-----------|-------------|-----------|
| 1 | 查看全部数据 | select *| pandas_name|
|2| 查看前n行数据| limit n|df.head(n)|
|3| 查询特定列| select 列名| df.loc[:,'列名']|
|4|  去重| distinct| unique|
|5| 条件| where| 指定条件  |
|6| 多条件同时满足| and| &|
|7| 多条件满足其一| or| | |
|8| 聚合操作| group by | groupby|
|9| 重命名| as|rename|
|10|连接|join| merge|
|11|左连接|left join|merge,how_left
|12|右连接|full join| merge,merge, hull|
|13|合并|concat|union all|
|14|合并去重|union | concat drop_duplicate |
|15|排序| order by| sort values|   
|16|条件操作分组| case when|map函数或者cut|
|17|更新 | 选择_赋值|update|
|18|删除行|delete| 选择相反条件|
|19|删除列|drop column| drop,axis=1|


