#!/usr/bin/env python
import pandas as pd

anaGood = pd.read_csv('testAnaGoodDiff.csv')
anaGoodSampled = anaGood.sample(n=2000, replace=False)

anaGoodSampled.to_csv('anaGoodSampled.csv')


