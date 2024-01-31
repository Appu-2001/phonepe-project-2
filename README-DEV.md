```bash
# 1.0 Creating virtual environment

python3 -m venv container --prompt="P2"
```

```bash
# 1.1 Installing dependencies

source container/bin/activate
python -m pip install -r requirements.txt
```

```bash
# 1.1.1 Listing installed dependencies

source container/bin/activate
python -m pip list
```

```bash
# 2.0 Cloning PhonePe Pulse repo

source container/bin/activate
python fetch.py
```

```bash
# 2.1 ETL PhonePe Pulse dataset

source container/bin/activate
python -m jupyter notebook setup.ipynb
```

```bash
# 3.0 Running app

source container/bin/activate
python -m streamlit run main.py
```
