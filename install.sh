git clone https://github.com/yastrab1/cookie-drepper
if ! command -v uv > /dev/null 2>&1
then
  curl -LsSf https://astral.sh/uv/install.sh | sh
fi

cd cookie-drepper
uv sync
uv run main.py