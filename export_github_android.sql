SELECT type, created_at, repository_owner, repository_name, 
       actor_attributes_email, actor_attributes_login, actor_attributes_name
FROM [githubarchive:github.timeline]
ORDER BY created_at, repository_name
WHERE repository_name="android" AND
    type != "WatchEvent" AND
    repository_owner IN (
      "github", "caseycrites", "mattr-", "atilacamurca", "burnsra", "arkangelkruel",
      "Sharc", "chrisrhoden", "avallark", "bharrat", "Beautyfree", "Schwanzerberg",
      "mablo", "hashbrown", "Tifancy", "cndoublehero", "emanonwzy", "lucasbrendel",
      "jjNford", "jalcine", "takiguchi0817", "yaioyaio", "tobibo", "ulinkwo",
      "prashanthr", "SteveVallay", "wugwei", "panhaidong", "dreamsxin", "breaklayer",
      "rakhmad", "iyedb", "andrebras", "chm090", "redshift13", "swapnarani", "kctang",
      "lt1946", "evoxmusic", "0nko", "crossle", "osvimer", "kkovach", "mwilson",
      "Kernald", "manigandan-balachandran", "ashwin91", "jisqyv", "jojosch",
      "pranavk", "fjfdeztoro", "Joxebus", "PKRoma", "weidiaoxiang", "huangbqsky",
      "apardo", "rainyin", "eniton", "jubic", "plause", "yccheok", "slynch13",
      "bkendzior", "vampelf", "dyf128", "dzwillpower", "Nordwin", "lemonkoala",
      "ahamlinman", "OnlyChristopher", "damor", "netojoaobatista", "a-thomas",
      "jmchuma", "RBEI-VENKAT", "xen0n", "imcaspar", "cored", "Rud5G", "oneill",
      "sm-pro", "VAlux", "chickenwin", "zcoder", "craigjennings11", "CNIAngel",
      "Bananeweizen", "dragsssss", "phuctbui", "bkuo", "icehong", "SkyKOG",
      "rookiepeng", "xiacl", "MastAvalons", "riousdelie", "joshpavlovich", "shingon",
      "dansondergaard", "kkelani", "dolanor", "iwaim", "eavgerinos", "faradaj",
      "try2try", "remomueller", "dai", "GuoYongxin", "miclovich", "omair", "NeilLi",
      "ksy5662", "williampratt", "webbertsai", "VladRassokhin", "ventrix",
      "JXPheonix", "Doomking", "huangcd", "afollestad", "devsundar", "3825", "5TDg9",
      "VenomVendor", "robbyoconnor", "behnam", "Coortouch", "INGBI", "Gopinathp",
      "kano556", "ricciardelli", "SeanWeber", "Adman", "dimaleonov", "jiajuntao",
      "Kribou", "hasija79", "4rk4nus", "herrsergio", "bazilio91", "cheesegrits",
      "Rakimior", "SarathSomana", "slarti88", "galois17", "weipoint", "garimagoswami",
      "astray0924", "carlloz", "xinyu1993abc", "TrevorBasinger", "keri12",
      "flada-auxv", "nedwidek", "ru-nekit-android", "McSun", "KWMalik", "Markmwaura",
      "gesellix", "haibocheng", "semihyagcioglu", "labotsirc", "nisal", "oocl",
      "jiangzhonghui", "akashasia", "sunnyhust2005", "vasc", "Ordosbxy", "royale1223",
      "WayneTatum", "herozhou1314", "shenzhun", "debmalyaroy", "doneill",
      "martinhath", "hornen", "lemalwoods", "wmjalak", "vovayatsyuk", "unixcrh",
      "feichangaihu", "jabbie", "loull521", "LuXIN", "zmqgithub", "kwonye",
      "pranaygunna", "strongyuen", "fegabe", "Justin7", "zhengyouxiang", "KingBright",
      "CinsonChen", "slapperwan", "newyork167", "chethanprabhakar", "yannux",
      "ThinkInChina", "w00d5t0ck", "pmekukka", "EugenZakharich", "wutong",
      "gjtorikian", "sagarsane", "ybq", "guhemama", "wufulin", "paicharan",
      "weitao2012", "zxcwillzxc", "abusalam", "lenshon", "sunandasaha", "haiger",
      "DerekLiu-", "jiemachina", "aya-eiya", "xzq2002", "Chiara-De-Liberato",
      "PTKDev", "coto", "CptnBrittish", "0x0001", "ygkee", "leeicoding"
    )
;

