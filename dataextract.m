minimum_spike_number = 200;
rat_name = 'Cor'
day_number_strings = {'01','02','03','04','05','06','07','08','09'};

mkdir(rat_name);

for day_index = 1:9
    day_number_string = day_number_strings{1,day_index};
    day_number = str2num(day_number_string)
    position_file = strcat(rat_name, '_raw/', rat_name,'pos', day_number_string, '.mat');
    spike_file = strcat(rat_name,'_raw/', rat_name,'spikes', day_number_string, '.mat');
    task_file = strcat(rat_name,'_raw/', rat_name,'task', day_number_string, '.mat');

    load(task_file);
    load(position_file);
    load(spike_file);

    task_dim = size(task{day_number});
    
    day_dir_name = strcat(rat_name, '/', rat_name, '_', num2str(day_number));
    dir_name = 'temp';
    
    mkdir(day_dir_name);
    process_file = fopen(strcat(day_dir_name,'/process_input.txt'),'w');
    fprintf(process_file, '%s\n', strcat(rat_name, '/', rat_name, '_', num2str(day_number), '/placefields.txt'));
    fprintf(process_file, 'track,day,epoch,unit,run_file,spike_file,smoothed_output_file,place_field_image\n');
    
    for epoch = 1:task_dim(2)
        track = 'sleep';
        dir_name = '';
        if isempty(task{day_number}{epoch})
            track = 'unknown';
            dir_name = strcat(rat_name, '_', num2str(day_number), '_', num2str(epoch));
            mkdir(day_dir_name,dir_name);
            mkdir(strcat(day_dir_name,'/',dir_name),'spikes');
            dlmwrite(strcat(day_dir_name, '/',dir_name,'/','run.txt'), pos{day_number}{epoch}.data(:,1:3),'precision',7);
            
        else
            if strcmp(task{day_number}{epoch}.type,'sleep')
                dir_name = strcat(rat_name, '_', num2str(day_number), '_', num2str(epoch), '_sleep');
                mkdir(day_dir_name,dir_name);
                mkdir(strcat(day_dir_name,'/',dir_name),'spikes');
                dlmwrite(strcat(day_dir_name, '/',dir_name,'/','run.txt'), pos{day_number}{epoch}.data(:,1:3),'precision',7);
            end

            if strcmp(task{day_number}{epoch}.type, 'run')
                track = task{day_number}{epoch}.description;
                dir_name = strcat(rat_name, '_', num2str(day_number), '_', num2str(epoch), '_run');
                mkdir(day_dir_name,dir_name);
                mkdir(strcat(day_dir_name,'/',dir_name),'spikes');
                dlmwrite(strcat(day_dir_name,'/',dir_name,'/','run.txt'), pos{day_number}{epoch}.data(:,1:3),'precision',7);
            end
        end
        
        mkdir(strcat(day_dir_name,'/',dir_name),'smoothed');
        mkdir(strcat(day_dir_name,'/',dir_name),'fields');

        tetrode_dim = size(spikes{day_number}{epoch});

        for tetrode = 1:tetrode_dim(2)
            unit_dim = size(spikes{day_number}{epoch}{tetrode});
            for unit = 1:unit_dim(2)
                if isempty(spikes{day_number}{epoch}{tetrode}{unit})
                    continue;
                end
                data_dim = size(spikes{day_number}{epoch}{tetrode}{unit}.data);
                if data_dim(1) > minimum_spike_number
                    fprintf(process_file, '%s,%i,%i,%i_%i,%s,%s,%s,%s\n', track, day_number,epoch,tetrode,unit,strcat(rat_name,'/',rat_name,'_', num2str(day_number),'/',dir_name,'/run.txt'),strcat(rat_name,'/',rat_name,'_', num2str(day_number),'/',dir_name,'/spikes/unit_', num2str(tetrode),'_',num2str(unit),'.txt'), strcat(rat_name,'/',rat_name,'_', num2str(day_number),'/',dir_name,'/smoothed/unit_', num2str(tetrode),'_',num2str(unit),'.txt'), strcat(rat_name,'/',rat_name,'_', num2str(day_number),'/',dir_name,'/fields/unit_', num2str(tetrode),'_',num2str(unit),'.bmp'));
                    filename = strcat(day_dir_name,'/',dir_name,'/spikes/unit_',num2str(tetrode),'_',num2str(unit),'.txt');
                    dlmwrite(filename, spikes{day_number}{epoch}{tetrode}{unit}.data(:,1),'precision',7);
                end
            end
        end
    end
    fclose(process_file);
end
status = 'Complete'