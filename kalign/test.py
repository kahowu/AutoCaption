from data import Kdata
from components.stft import Stft
from components.istft import Istft
from components.rpca import Rpca
from components.smoothing import Smoothing


if __name__ == "__main__":
    filename = "../data/test.wav"
    kdata = Kdata(filename)
    stftComponent = Stft()
    stftComponent.run(kdata)

    rpcaComponent = Rpca(mu_fac=125, rho=1.5)
    rpcaComponent.run(kdata)

    istftComponent = Istft()
    istftComponent.run(kdata)

    smoothingComponent = Smoothing()
    smoothingComponent.run(kdata)

    # print "Playing instrumental"
    # kdata.play("instrumental")

    # print "playing vocal"
    # kdata.play("smoothedVocal")
    kdata.save("smooth_bob.wav", "smoothedVocal")
