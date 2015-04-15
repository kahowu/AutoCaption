% This is an example code for running the RPCA for source separation
% P.-S. Huang, S. D. Chen, P. Smaragdis, M. Hasegawa-Johnson, 
% "Singing-Voice Separation From Monaural Recordings Using Robust Principal Component Analysis," in ICASSP 2012
%
% Written by Po-Sen Huang @ UIUC
% Modified by Jeff Wu
% For any questions, please email to huang146@illinois.edu.

%% addpath
function [SDR,SIR,SAR] = rpca_mask_bss(filename)
clearvars -except filename; 
close all; 
addpath('bss_eval');
addpath(genpath('inexact_alm_rpca'));


%% Examples
% filename='yifen_2_01';
wavinA= wavread(['original_instrumental', filesep, filename,'_instrumental.wav']);
wavinE= wavread(['original_vocal', filesep, filename,'_vocal.wav']);
rpcaA= wavread(['rpca_instrumental', filesep, filename,'_instrumental.wav']);
rpcaE= wavread(['rpca_vocal', filesep, filename,'_vocal.wav']);

wavlength=length(wavinA);

% GNSDR computation
% [wavinmix,Fs]= wavread(['music', filesep, filename,'.wav']);
% [e1,e2,e3] = bss_decomp_gain( wavinmix', 1, wavinE');
% [sdr_,sir_,sar_] = bss_crit( e1, e2, e3);
% GNSDR computation

%% BSS Evaluation
Parms=bss_evaluate(wavinA,wavinE, rpcaA, rpcaE); % SDR(\hat(v),v),                    

% %% NSDR=SDR(estimated voice, voice)-SDR(mixture, voice)
% NSDR=Parms.SDR-sdr_;
%%        

SDR=Parms.SDR;
SIR=Parms.SIR;
SAR=Parms.SAR;
fprintf('SDR:%f\nSIR:%f\nSAR:%f\n',Parms.SDR,Parms.SIR,Parms.SAR);