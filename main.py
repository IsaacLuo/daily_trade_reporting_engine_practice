from generate_sample_data import generate_sample_data
from generate_report import generate_report

if __name__ == '__main__':
    data = generate_sample_data(1000)
    generate_report(data)
    