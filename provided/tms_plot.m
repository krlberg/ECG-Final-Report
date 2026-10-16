%
% Deze m-file plot meerdere kanalen van de Portilab data-file in een plot
% This m-file plot various channels of the PolyBench data-file in a plot
%
fname=input('Filename : ','s');
portidata=tms_read(fname)                       		% This file reads the TMSi data file <<filename>>.Poly5
tstep=1/portidata.header.FS;                        	% Set the timestap, derived from the sample frequency stored in the header of the PolyBench data file.
tend=tstep*(portidata.header.NumberOfSamplePeriods-1);	% Calculate the stop time from the step size and the number of samples
t=(0:tstep:tend);                                   	% make the time-array
pmin=input('Lowest channel number: ');             			% Select range of channels to plot (1-4)
pmax=input('Highest channel number: ');
n=input('Number of columns for plot-array: ');         		% Determine the dimension of the plotarray bij chosing the number of columns (2)
m=ceil((pmax-pmin+1)/n);                            	% Calculate the numver of rows (must be an interger number)
for p = 1:(pmax-pmin+1)                             	% plot the data array in a loop
    signalname=portidata.description(1,p+pmin-1).SignalName';	% Extract the channel name from the file header
    subplot(m,n,p);                                 	% 
    plot(t,portidata.data{p+pmin-1,1});            		% plot the channel
    grid on;                                            % switch on the grid
    xlabel('t [s]');                                	% add axis labels
    ylabel(signalname);
end