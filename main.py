from src.tasks import task
from src.logic.helpers.validator import validate_parameters

def main():
  validate_parameters()
  task()

if __name__ == '__main__':
  main()