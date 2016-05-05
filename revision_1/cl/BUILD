# Author: prasenjtj@google.com (Prasenjit Jana)

py_binary(
    name = "sports_roster",
    srcs = ["sports_roster.py"],
    deps = [
            "soccer_thali",
            ":nfl_thali",
            ":nhl_thali",
            ":nba_thali",
            ":mlb_thali",
            "//pyglib",
            ]
)

py_binary(
    name = "mlb_thali",
    srcs = ["mlb_thali.py"],
    deps = [""//pyglib"],
)

py_binary(
    name = "nba_thali",
    srcs = ["nba_thali.py"],
    deps = [""//pyglib"],
)

py_binary(
    name = "nfl_thali",
    srcs = ["nfl_thali.py"],
    deps = [""//pyglib"],
)

py_binary(
    name = "nhl_thali",
    srcs = ["nhl_thali.py"],
    deps = [""//pyglib"],
)
