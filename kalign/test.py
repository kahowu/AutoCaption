from data import Kdata
from components.stft import Stft
from components.istft import Istft
from components.rpca import Rpca


if __name__ == "__main__":
    # kdatabase = Kdatabase("../data", is_mk1_data=True)
    # for i in kdatabase.get_data():
    #     import pdb; pdb.set_trace();
    kdata = Kdata("../data/titon_2_07_SNR5.wav")
    stftComponent = Stft()
    stftComponent.run(kdata)

    rpcaComponent = Rpca(tol=1e-4)
    rpcaComponent.run(kdata)

    istftComponent = Istft()
    istftComponent.run(kdata)

    import pdb; pdb.set_trace();    
    kdata.play("istft")
