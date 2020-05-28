from analysis import MM
import pickle


def show_stats():
    try:
        with open('db.dat', 'rb') as file:
            db = pickle.load(file)
    except IOError:
        print("No database file")
        return None
    db.get_stats()


if __name__ == "__main__":
    show_stats()
