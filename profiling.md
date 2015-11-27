# Integrated Profiling tools

Within the python standard library, there is basic profiling support via the modules `cProfile` and `profile`. (cf. the [Python Help Ch. 27.4](https://docs.python.org/3.4/library/profile.html))
These profilers generally only time the execution time of individual functions. Most of the time it is more useful to get profiling on the line level within individual functions. A solution for this which is apparently high regarded is [line_profiler by Robert Kern](https://github.com/rkern/line_profiler).

Contrary what one findes in parts of the [README](https://github.com/rkern/line_profiler/blob/master/README.rst), according to the last question in the [FAQ](https://github.com/rkern/line_profiler/blob/master/README.rst#frequently-asked-questions) it is tested agains python 2.7 as well as 3.2-3.4 (cf. also the [1.0 Release Notes](https://github.com/rkern/line_profiler/blob/master/README.rst#10).

# Working on issue #64

I used the minimal example from issue #64 as found in file `issue_64_minimal_example.py` in commit a1c2154. 

To profile a part of a script, we need to wrap it in a function, on which we use the decorator `@profile` (do not forget to actually call this function; cf. commit 5b37768) and then run in the command line:
```bash
$ kernprof -l issue_64_minimal_example.py
```
and then after execution run the following command to show the results:
```bash
$ python -m line_profiler issue_64_minimal_example.py.lprof
```
The result then looks somewhat like this:
```
Timer unit: 1e-06 s

Total time: 3.36461 s
File: issue_64_minimal_example.py
Function: test_the_history at line 23

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
    23                                           @profile
    24                                           def test_the_history():
    25         1           11     11.0      0.0         container = EpexHistoryContainer(history_specs, None, source_start, 'minute',
    26         1      3336655 3336655.0     99.2                                         env=env)
    27                                           
    28         1            8      8.0      0.0         data = {}
    29         1           35     35.0      0.0         data[1] = {'dt': pd.Timestamp('2015-06-27'),
    30         1           18     18.0      0.0                    'price': np.random.uniform(0, 100),
    31         1            3      3.0      0.0                    'market': 'epex_auction',
    32         1            3      3.0      0.0                    'product': '00-01',
    33         1            7      7.0      0.0                    'day': pd.Timestamp('2015-06-27'),
    34         1            5      5.0      0.0                    'sid': 1}
    35         1            6      6.0      0.0         data[2] = {'dt': pd.Timestamp('2015-06-26'),
    36         1            4      4.0      0.0                    'price': np.random.uniform(0, 100),
    37         1            2      2.0      0.0                    'market': 'epex_auction',
    38         1            2      2.0      0.0                    'product': '00-01',
    39         1           25     25.0      0.0                    'day': pd.Timestamp('2015-06-26'),
    40         1            5      5.0      0.0                    'sid': 2}
    41         3           17      5.7      0.0         for current_sid in data:
    42         2            8      4.0      0.0             current_data = data[current_sid]
    43         2           23     11.5      0.0             bar = BarData({current_sid: current_data})
    44         2         9497   4748.5      0.3             container.update(bar, current_data['dt'])
    45                                           
    46         1           13     13.0      0.0         history = container.get_history()
    47                                           
    48         1        18262  18262.0      0.5         print(history['epex_auction'])
```

After having also decorated the functions `frame_from_bardata` and `add_frame` in `powerline/gg/powerline/history/history_container.py` with `@profile` the end result is:
```
Timer unit: 1e-06 s

Total time: 0.002584 s
File: /home/dev/powerline/pow-aws/gg/powerline/history/history_container.py
Function: frame_from_bardata at line 36

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
    36                                               @profile
    37                                               def frame_from_bardata(self, data, algo_dt):
    38                                                   """Create a DataFrame from the given BarData and algo dt."""
    39         2            4      2.0      0.2          data = data._data
    40         2            5      2.5      0.2          frame_data = {}
    41                                           
    42         4           13      3.2      0.5          for sid in data:
    43         2            5      2.5      0.2              event = data[sid]
    44         2           10      5.0      0.4              if algo_dt != event['dt']:
    45                                                           continue
    46                                           
    47         2            4      2.0      0.2              market = event['market']
    48         2            6      3.0      0.2              if market in ['cascade', 'auction_signal']:
    49                                                           continue
    50                                           
    51         2            5      2.5      0.2              day = event['day']
    52         2            4      2.0      0.2              product = event['product']
    53                                           
    54                                                       # Add a market to the frame_data if it is not already listed
    55         2            8      4.0      0.3              if market not in frame_data.keys():
    56         2            8      4.0      0.3                  frame_data.update({market: {}})
    57                                           
    58                                                       # Try adding an individual product price to a day's dict
    59         2            6      3.0      0.2              try:
    60         2           21     10.5      0.8                  frame_data[market][day].update({product: event['price']})
    61                                                       # if the day is not yet listed, create it
    62         2            8      4.0      0.3              except KeyError:
    63         2           13      6.5      0.5                  frame_data[market].update({day: {product: event['price']}})
    64                                           
    65         2            6      3.0      0.2          if not frame_data:
    66                                                       return None
    67                                           
    68         2            6      3.0      0.2          frame = {}
    69         4           15      3.8      0.6          for market in frame_data.keys():
    70                                                       # Create pandas DataFrames for the individual markets
    71         2           11      5.5      0.4              frame.update({market: pd.DataFrame.from_dict(frame_data[market],
    72         2         2420   1210.0     93.7                                                           'index')})
    73                                                       # TODO for continuous intrady this needs to be a Panel
    74         2            6      3.0      0.2          return frame

Total time: 0.007061 s
File: /home/dev/powerline/pow-aws/gg/powerline/history/history_container.py
Function: add_frame at line 84

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
    84                                               @profile
    85                                               def add_frame(self, frame, env=None):
    86         2            6      3.0      0.1          if frame is None:
    87                                                       return
    88         4           12      3.0      0.2          for id in frame.keys():
    89         2            5      2.5      0.1              if frame[id] is None:
    90                                                           continue
    91         2           15      7.5      0.2              if len(self.rolling_frame[id]) == 0:
    92         1            3      3.0      0.0                  self.rolling_frame[id] = self.rolling_frame[id].append(
    93         1         4386   4386.0     62.1                      frame[id])
    94                                                       else:
    95         1           67     67.0      0.9                  if frame[id].index[0] in self.rolling_frame[id].index:
    96                                                               self.rolling_frame[id].\
    97                                                                   update(frame[id])
    98                                                           else:
    99         1            3      3.0      0.0                      self.rolling_frame[id] = self.rolling_frame[id].append(
   100         1         2549   2549.0     36.1                          frame[id])
   101                                           
   102         2           15      7.5      0.2              if len(self.rolling_frame[id]) > self.length:
   103                                                           self.rolling_frame[id] = self.rolling_frame[id].\
   104                                                               drop(self.rolling_frame[id].
   105                                                                    index[0:(len(self.rolling_frame[id])-self.length)])

Total time: 3.44158 s
File: issue_64_minimal_example.py
Function: test_the_history at line 23

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
    23                                           @profile
    24                                           def test_the_history():
    25         1            4      4.0      0.0         container = EpexHistoryContainer(history_specs, None, source_start, 'minute',
    26         1      3413346 3413346.0     99.2                                         env=env)
    27                                           
    28         1            7      7.0      0.0         data = {}
    29         1           32     32.0      0.0         data[1] = {'dt': pd.Timestamp('2015-06-27'),
    30         1           19     19.0      0.0                    'price': np.random.uniform(0, 100),
    31         1            3      3.0      0.0                    'market': 'epex_auction',
    32         1            3      3.0      0.0                    'product': '00-01',
    33         1            8      8.0      0.0                    'day': pd.Timestamp('2015-06-27'),
    34         1            5      5.0      0.0                    'sid': 1}
    35         1            6      6.0      0.0         data[2] = {'dt': pd.Timestamp('2015-06-26'),
    36         1            4      4.0      0.0                    'price': np.random.uniform(0, 100),
    37         1            3      3.0      0.0                    'market': 'epex_auction',
    38         1            2      2.0      0.0                    'product': '00-01',
    39         1            6      6.0      0.0                    'day': pd.Timestamp('2015-06-26'),
    40         1            4      4.0      0.0                    'sid': 2}
    41         3           11      3.7      0.0         for current_sid in data:
    42         2            5      2.5      0.0             current_data = data[current_sid]
    43         2           20     10.0      0.0             bar = BarData({current_sid: current_data})
    44         2         9902   4951.0      0.3             container.update(bar, current_data['dt'])
    45                                           
    46         1            5      5.0      0.0         history = container.get_history()
    47                                           
    48         1        18187  18187.0      0.5         print(history['epex_auction'])
```


# Other remarks

In the professional edition of PyCharm, since 4.5 there is a graphical profiling tool integrated into the IDE.
