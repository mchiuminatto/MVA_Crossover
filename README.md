# Outliers are Liars

Author: Marcello Chiuminatto <br>
Python version: 3.10.4


## Overview

In the context of FOREX trading, in the commitment for finding profitable trading strategies, you will find in books, articles, papers, web sites and maybe from your own inspiration, strategies that shows positive profits, based on cumulative profit over a period. Well, that is not enough unfortunately, because does not necessarily indicate consistency in the profits.

Would be profit average (expected profit) then be a good indicator of profits consistency? The answer is not straight forward: not necessarily. Why? and the answer to this question is the topic of this publication: Outliers. 

Outliers will distort the reading of cumulative profits and expected profits in such a way that a losing strategy, can look like a profitable one.

Consider the following example:
Let's define a strategy S, from which we get a sample of 50 trades whose profits are distributed as shown in the next table:



|        |Trades | Profit/trade[pips] |Total Profit[pips]|
|--------| ------|--------------------|------------------|
|        |  25   |   -5.0             |        -125.0    |    
|        |  24   |   2.0              |          48.0    |
|        |  1    |  200.0             |         200.0    |
|--------|-------|--------------------|-------------------
| Total  |  50   |                    |         123.0    |
| mean   |       |                    |         2.5      |
| median |       |                    |         -1.5     |



Total profit and average profit are positive, but clearly this is strongly influenced by the 200 pip trade. Pay close attention to median though, is telling something about this case.

Based on a real but simple trading strategy, it will be shown how outliers impacts mean and total profits, however median signals that something is hiding behind the scenes.

Throughout this article, it will be shown with a real, but simple trading strategy, the danger of not paying attention to outliers and in the process of showing so, it is presented the trading strategy research life cycle: design / back-testing, analysis, and conclusions.


## Strategy Design

### Definitions and Concepts

This strategy is one of the simplest trend-following or momentum FOREX trading strategy.

For simplicity, this analysis focuses only on buying (long) strategy.

The rationale behind the strategy is the following: *“When price “accelerates” enough to the upside it is likely that will remain that way for a while, so is a good signal for opening a buying position and keep it open until market decelerate.”*

To have an actionable and testable strategy is necessary to define in mathematical terms the concepts involved in the above statement: acceleration and deceleration. It necessary to remark that these concepts are defined in the context of this trading strategy analysis only and under no way are general concepts that can necessarily be applied to ALL trading strategies or financial markets.

Being that said and reducing the abstraction level a bit, market acceleration is defined as: when prices close above a fast-moving average, which is above a medium-moving average, which at the same time is above a slow-moving average.

Market deceleration is defined as: when the fast-moving average cross below the medium-moving average.

**What is a Moving Average (MA) of $n$ periods?**

It is the average of the last $n$ available price periods. Generally, is calculated on close price (which is the case for this research), but can also be calculated on open, high, low, typical price etc.)


Mathematically:

$MA(close;n)=\frac{1}{n}\sum_{i=t-n+1}^{i=0} close_i$


*Simple moving average on close parametrized with n (periods)*

Where:

- $n$ Number of periods
- $close_i$: close price at i-th period


*What are fast, medium and slow moving averages?*

The concept of speed for a MA's is given by the number of periods the MA is calculated on; less number periods will make the MA to react *faster* to price action whilst greater number of periods will make it *slower*.

In this context the periods for the three different MA are defined as follows:

* Fast MA ($MA_f$): 10 periods
* Medium MA ($MA_m$): 25 periods
* Slow MA ($MA_s$): 50 periods


### Long entry/exit rules

Now it is time to concretely define the strategy Entry/Exit/Management rules.

 **Entry**<br><br>
  Enter long when close cross above $SMA_f$ and $SMA_f$ is above $SMA_m$ and $SMA_m$ is above $SMA_s$
  
  Mathematically:
  
  Enter long when the following two conditions are true
  
  1. $close_{t-1}<SMA_f \land close_t > SMA_f$
  2. $SMA_s < SMA_m < SMA_f$
 
  **Exit**<br><br> 
  Exit a long position when $SMA_f$ cross below $SMA_m$

  Mathematically

  Exit when
  1. $SMA_f < SMA_m$
   
<img src="./long_setup_example.png">


## Strategy Back-Testing

Strategy back-testing is in essence simulating the strategy logic on historic data, expecting that past performance will repeat in the feature. But this is not necessarily the case and depends a lot on how the back-testing process is designed and executed, among other conditions. Detailed back-testing discussion is out of the scope of this analysis. As a starter you can find more here: https://www.investopedia.com/terms/b/backtesting.asp.

What is relevant for this analysis is that back-testing will produce a set of trades that if considered right out of the process they seem to be produced by a profitable strategy, but hypothetically this is not true and the real losing results are hidden by outliers.

In this section are presented some steps to implement a simple *vectorized* back-testing process. The term **vectrorized** means that instead of looping throughout the elements of an array or a matrix performing scalar operations, the operations are performed on entire arrays or matrices (vectors). Why to do so? because the reduction of processing time is significant, specially when working with millions or billions of records. You can find more here: https://www.youtube.com/watch?v=BR3Qx9AVHZE

### Data

This study is based on FOREX data for the instrument EURUSD, format OHLC (Open/High/Low/Close) aggregated at a fix frequency of one hour (H1) in the period from 2015-01-01 22:00:00 until 2021-11-24 23:00:00

Sample:

| Time (UTC) | Open | High | Low | Close | Volume |
| --- | --- | --- | --- | --- | --- |
| 2021-11-24 19:00:00 | 1.11925 | 1.12034 | 1.11883 | 1.11985 | 3332.690 |
| 2021-11-24 20:00:00 | 1.11984 | 1.12053 | 1.11976 | 1.12050 | 1500.710 |
| 2021-11-24 21:00:00 | 1.12049 | 1.12054 | 1.11962 | 1.11962 | 1051.825 |
| 2021-11-24 22:00:00 | 1.11957 | 1.12020 | 1.11944 | 1.12001 | 662.320 |
| 2021-11-24 23:00:00 | 1.11997 | 1.12042 | 1.11997 | 1.12025 | 465.710 |



![image](https://user-images.githubusercontent.com/9592242/171404656-c2cbc79a-c480-4770-8022-1088b2a3f626.png)

