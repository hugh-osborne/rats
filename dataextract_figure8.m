
experiment_name = 'i01_maze09_MS.002';
behav_file = strcat(experiment_name, '_raw/', experiment_name, '_BehavElectrDataLFP.mat');
pos_file = strcat(experiment_name, '_raw/', experiment_name, '_1250Hz.whl.interp.mat');

try
load(behav_file);
catch
    disp('failed to properly load behaviour file - attempting to continue.');
end

load(pos_file);

pos_count = size(XMiddleLed);
pos = [(1:pos_count)', XMiddleLed, YMiddleLed];

pos_trim = pos(pos(:,2) > 0.0 & pos(:,3) > 0.0,:);
pos_trim_dim = size(pos_trim);

mkdir(experiment_name);
mkdir(experiment_name, 'spikes');
mkdir(experiment_name, 'smoothed');
mkdir(experiment_name, 'fields');

process_file = fopen(strcat(experiment_name,'/process_input.txt'),'w');
fprintf(process_file, '%s\n', strcat(experiment_name, '/placefields.txt'));
fprintf(process_file, 'track,day,epoch,unit,run_file,spike_file,smoothed_output_file,place_field_image\n');

dlmwrite(strcat(experiment_name, '/run.txt'), pos_trim,'precision',8);

for cluster_num = 33:106
    cluster_num_string = num2str(cluster_num);
    spks = Spike.res(Spike.totclu == cluster_num);
    fprintf(process_file, '%s,%i,%i,%i,%s,%s,%s,%s\n', 'figure8', 0,0,cluster_num,strcat(experiment_name,'/run.txt'),strcat(experiment_name,'/spikes/unit_', num2str(cluster_num),'.txt'), strcat(experiment_name, '/smoothed/unit_', num2str(cluster_num),'.txt'), strcat(experiment_name, '/fields/unit_',num2str(cluster_num),'.bmp'));
    dlmwrite(strcat(experiment_name, '/spikes/unit_', cluster_num_string,'.txt'), spks(spks(:) > pos_trim(1,1) & spks(:) < pos_trim(pos_trim_dim(1),1)), 'precision', 8);
end

fclose(process_file);
status = 'Complete'