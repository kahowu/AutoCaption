from data import Kdatabase

if __name__ == "__main__":
    kdatabase = Kdatabase("../data", is_mk1_data=True)
    for i in kdatabase.get_data():
        import pdb; pdb.set_trace();
    
