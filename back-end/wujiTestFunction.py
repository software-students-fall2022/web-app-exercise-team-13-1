from flask import Flask, render_template, request, redirect, url_for, make_response
from dotenv import dotenv_values


import pymongo
import datetime
from bson.objectid import ObjectId
import sys

temp=1;
def wuji():
    print(temp);
    return
