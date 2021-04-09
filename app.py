# import statements

import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

from flask import Flask, jsonify

# taken from day 3 activity 10
engine = create_engine("sqlite:///hawaii.sqlite")


Base = automap_base()

Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station