# simpleChat-Streamlit

Unified interface where you can run Benchmarking on any deployed text based Large Language Model or run chat service.

### Note

- For benchmarking, the dataset should be json file of the format:
```
[
    {
        "input":"Prompt based on finetuned task of LLM",
        "instruction": "Specific instruction to the model",
        "output": "Expected output from the model"
    },
    {
        ...
    },
    ...
]
```

- The application is still in development, you might face glitches when reruning the benchmarks. Reloading the page is one of the option.

## Steps:

- Install the requirements using requirements.txt:

    ```pip install -r requirements.txt```

- Create a `.env` file containing the URL to which the request is to be posted in a variable `URL`.
- Launch the python file using `streamlit run main.py`
- Upon launching the interface, you can give prompts for the task which the Large Language Model is trained on.

## Outputs:

### Chat Output

![image](https://github.com/anandhu-eng/simpleChat-Streamlit/assets/71482562/29bff483-c2a3-489c-8815-1a21fae36641)

![image](https://github.com/anandhu-eng/simpleChat-Streamlit/assets/71482562/80b3718e-3e52-419f-9a17-4bbd9ba0d07f)

### Benchmarking Output

Note that the video is fast forwarded to eliminate lag in loading and processing period.







https://github.com/anandhu-eng/simpleChat-Streamlit/assets/71482562/308fb9c6-62a8-41b6-99ba-69eadf9e21c0




