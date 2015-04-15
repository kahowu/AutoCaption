% Written by Jeff Wu

function Parms=bss_evaluate(wavinA,wavinE,rpcaA, rpcaE)
    %% evaluate
    if length(rpcaA)==length(wavinA)
        sep = [rpcaA , rpcaE]';
        orig = [wavinA , wavinE]';

        for i = 1:size( sep, 1)
               [e1,e2,e3] = bss_decomp_gain( sep(i,:), i, orig);
               [sdr(i),sir(i),sar(i)] = bss_crit( e1, e2, e3);
        end
    else
        minlength=min( length(rpcaE), length(wavinE) );

        sep = [rpcaA(1:minlength) , rpcaE(1:minlength)]';
        orig = [wavinA(1:minlength) , wavinE(1:minlength)]';

        for i = 1:size( sep, 1)
               [e1,e2,e3] = bss_decomp_gain( sep(i,:), i, orig);
               [sdr(i),sir(i),sar(i)] = bss_crit( e1, e2, e3);
        end
    end

    Parms.SDR=sdr(2);
    Parms.SIR=sir(2);
    Parms.SAR=sar(2);
