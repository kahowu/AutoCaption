from data import Kdata
from components.stft import Stft
from components.istft import Istft
from components.rpca import Rpca


if __name__ == "__main__":
    filename = "../data/bob_dyl.mp3"
    kdata = Kdata(filename)
    stftComponent = Stft()
    stftComponent.run(kdata)

    rpcaComponent = Rpca(mu_fac=1.25, rho=1.5, debug=True)
    rpcaComponent.run(kdata)

    istftComponent = Istft()
    istftComponent.run(kdata)

    print "Playing instrumental"
    kdata.play("instrumental")

    print "playing vocal"
    kdata.play("vocal")

