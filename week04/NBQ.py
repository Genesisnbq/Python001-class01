import pandas as pd


data = pd.DataFrame()
table1 = pd.DataFrame()
table2 = pd.DataFrame()

# 1. SELECT * FROM data;
data

# 2. SELECT * FROM data LIMIT 10;
data.iloc[:10, :]

# 3. SELECT id FROM data;  //id 是 data 表的特定一列
data['id']

# 4. SELECT COUNT(id) FROM data;
data.shape[0]

# 5. SELECT * FROM data WHERE id<1000 AND age>30;
cond1 = data['id'] < 1000
cond2 = data['age'] > 30
data[cond1 & cond2]

# 6. SELECT id,COUNT(DISTINCT order_id) FROM table1 GROUP BY id;
data.groupby('id').agg(
    {
        'id': 'first',
        'order_id': 'nunique'
    }
)

# 7. SELECT * FROM table1 t1 INNER JOIN table2 t2 ON t1.id = t2.id;
pd.merge(table1, table2, on='id', how='inner')

# 8. SELECT * FROM table1 UNION SELECT * FROM table2;
table1.append(table2)

# 9. DELETE FROM table1 WHERE id=10;
table1.drop(10, inplace=True)

# 10. ALTER TABLE table1 DROP COLUMN column_name;
table1.drop('column_name', axis=1, inplace=True)
