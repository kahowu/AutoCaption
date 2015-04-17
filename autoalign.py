from kalign.data import Kdata
from kalign.components.stft import Stft
from kalign.components.istft import Istft
from kalign.components.rpca import Rpca
from kalign.components.smoothing import Smoothing
from kalign.components.smoothing import Smoothing
import glob

if __name__ == "__main__":
    path = "Data/"

    for filename in glob.glob(path + "*"):
        # filename = path + "segment_01.wav"
        kdata = Kdata(filename)
        kdata["vocal"] = kdata["input"]
        # stftComponent = Stft()
        # stftComponent.run(kdata)
        # rpcaComponent = Rpca(mu_fac=125, rho=1.5)
        # rpcaComponent.run(kdata)
        # istftComponent = Istft()
        # istftComponent.run(kdata)
        smoothingComponent = Smoothing(debug=True, threshold=0.05)
        smoothingComponent.run(kdata)
        #kdata.play("smoothedVocal")
        converted_filename = path + "smooth/" + filename[5:]  
        kdata.save(converted_filename, "smoothedVocal")
