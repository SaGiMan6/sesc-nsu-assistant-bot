import asyncio

import aiohttp

import pandas as pd

from io import StringIO


async def download_table():
  url = "https://docs.google.com/spreadsheets/u/0/d/e/2PACX-1vQdS9Qd6cdKjcvTefM_PaaODSfpkpk55Zl2g4QxBVpKkUJsU1U08wKXdi6cSkNBAQ/pubhtml"
  async with aiohttp.ClientSession() as session:
    async with session.get(url) as response:
      html = await response.text()
  return pd.read_html(StringIO(html), header=1, encoding="utf-8")[0]


def get_day(df, column_name, day_of_week):
  d = df.loc[:,column_name][13*day_of_week+2:13*day_of_week+14]
  lessons = [str(d.iloc[0]), str(d.iloc[4]), str(d.iloc[8])]
  for i in range(len(lessons)):
    lessons[i] = lessons[i].upper()
  changes = ["АНГЛ", "ИСТ", "ЛИТ", "РУС", "ГЕО", "ОБЩ"]
  for i in range(len(lessons)):
    for j in changes:
      if lessons[i].find(j) != -1:
        lessons[i] = j
  for i in range(len(lessons)):
    if lessons[i] == "NAN":
      lessons[i] = "—"
  cabinets = [str(d.iloc[1])[-3:], str(d.iloc[5])[-3:], str(d.iloc[9])[-3:]]
  for i in range(len(cabinets)):
    if cabinets[i] == "nan":
      cabinets[i] = "—"
  return [[lessons[i], cabinets[i]] for i in range(len(cabinets))]


def get_column(df, name):
  return dict((str(i), get_day(df, name, i)) for i in range(6))


def get_table(df):
  d = df.loc[0][4:]
  d = d[~d.isnull()]
  result = {}
  l = 0
  while l < len(d):
    k = 0
    m = {str(d.iloc[l+k])[-3:]: get_column(df, str(d.index[l+k]))}
    k = 1
    c = str(d.index[l]).split(".")[0]
    while l + k < len(d) and c == str(d.index[l+k]).split(".")[0]:
      m.update( {str(d.iloc[l+k])[-3:]: get_column(df, str(d.index[l+k]))} )
      k += 1
    l += k
    result.update({c: m})
  return result


async def download_timetable():
  df = await download_table()
  return get_table(df)

if __name__ == "__main__":
  r = asyncio.run(download_timetable())
  print(r)
  print(r["11_10"]["322"]["3"])
