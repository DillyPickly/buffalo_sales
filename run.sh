#!/bin/bash
nohup bokeh serve buffalo_sales --port 5100 --log-level=info --allow-websocket-origin='dylansabuda.com' &