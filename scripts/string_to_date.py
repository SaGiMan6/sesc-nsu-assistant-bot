from datetime import datetime

from re import match, sub


def string2date(string: str):
    string = string.lower()
    date = datetime.now().strftime(r"%d %m %y").split()
    phrases = ["вч", "зав"]
    pref = ["поза", "после"]
    for j in range(len(phrases)):
        if string.find(phrases[j]) != -1:
            delta_days = -1 - string.count(pref[j])
            if phrases[j] == "зав":
                delta_days *= -1
            day = int(datetime.now().strftime(r"%j"))
            day += delta_days
            return datetime.strptime(str(date[2]) + str(day), "%y%j")
    else:
        months = ["янв", "фев", "мар", "апр", "май", "июн", "июл", "авг", "сен", "окт", "ноя", "дек"]
        for i in range(len(months)):
            if string.find(months[i]) != -1:
                date[1] = str(i)
        string = sub(r"[^\d]", r" ", string).strip().split()
        for i in range(len(string)):
            date[i] = string[i]
        if match(r"\d\d\d\d", date[2]):
            string[2] = date[2][-2:]
        return datetime(int(date[2]), int(date[1]), int(date[0]))


if __name__ == "__main__":
    for i in ["02.09.23", "02.09.2023", "02.09", "02 9.23", " 2  9 23 nlkgfkg", "02", "2 Декабря", "Сент 3", "сен",
              "завтра", "вчера", "послезавтра", "позавче", "Послепослезавтра", "поза" * 50 + "вч"]:
        print(string2date(i).strftime(r"%d.%m.%y"), "==", i)
