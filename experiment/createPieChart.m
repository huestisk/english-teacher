function createPieChart(col, data, plotTitle, byGroup)
%UNTITLED Summary of this function goes here
%   Detailed explanation goes here

fontsize = 16;
max_width = 16;
main = categorical(data.(col));
labels = categories(main);

len = 0;
words = split(plotTitle);
if length(words) > 1
    for k = 1:length(words)
        word = words{k};
        if len == 0
            wrappedTitle = word;
            len = length(word);
        elseif len < 30
            wrappedTitle = strcat(wrappedTitle, " ", word);
            len = len + length(word);
        else
            wrappedTitle = strcat(wrappedTitle, string(newline), word);
            len = 1;
        end
    end
    plotTitle = wrappedTitle(1);
end

if byGroup
    
    chart2 = categorical(data{data{:,"Var3"}=="Group 1",col});
    chart3 = categorical(data{data{:,"Var3"}=="Group 2",col});
    chart4 = categorical(data{data{:,"Var3"}=="Group 3",col});

    counts = zeros(numel(labels), 4);
    for i = 1:numel(labels)
        label = labels{i};
        counts(i,1) = sum(main(:)==label);
        counts(i,2) = sum(chart2(:)==label);
        counts(i,3) = sum(chart3(:)==label);
        counts(i,4) = sum(chart4(:)==label);
    end

    t = tiledlayout(2,2, 'TileSpacing', 'compact');

    nexttile, h1=pie(counts(:,1)); title("All",'FontSize',fontsize-2)
    nexttile, h2=pie(counts(:,2)); title("Group 1",'FontSize',fontsize-2)
    nexttile, h3=pie(counts(:,3)); title("Group 2",'FontSize',fontsize-2)
    nexttile, h4=pie(counts(:,4)); title("Group 3",'FontSize',fontsize-2)

    % Fix Labels
    set(h1(2:2:end),'FontSize',fontsize-4);
    set(h2(2:2:end),'FontSize',fontsize-4);
    set(h3(2:2:end),'FontSize',fontsize-4);
    set(h4(2:2:end),'FontSize',fontsize-4);
    
    for idx = 2:2:length(h1)
        if h1(idx).String == "0%"
            h1(idx).String = '';
        end
    end
    
    for idx = 2:2:length(h2)
        if h2(idx).String == "0%"
            h2(idx).String = '';
        end
    end
    
    for idx = 2:2:length(h3)
        if h3(idx).String == "0%"
            h3(idx).String = '';
        end
    end
    
    for idx = 2:2:length(h4)
        if h4(idx).String == "0%"
            h4(idx).String = '';
        end
    end
    
    % create legend
    for i = 1:length(labels)
        labels{i} = erase(labels{i}, " years old");
    end
    
    
    for i = 1:length(labels)
        label = split(labels{i});
        len = 0;
        if length(label) > 1
            for k = 1:length(label)
                word = label{k};
                if len == 0
                    wrappedLabel = word;
                    len = length(word);
                elseif len < max_width
                    wrappedLabel = strcat(wrappedLabel, " ", word);
                    len = len + length(word);
                else
                    wrappedLabel = strcat(wrappedLabel, string(newline), word);
                    len = 1;
                end
            end
            labels{i} = wrappedLabel(1);
        end
    end
        
    lg = legend(nexttile(2),labels,'FontSize',fontsize-4);
    lg.Location = 'northeastoutside';

    title(t, plotTitle, 'FontSize', fontsize);
    
else
    
    counts = zeros(numel(labels),1);
    for i = 1:numel(labels)
        label = labels{i};
        counts(i,1) = sum(main(:)==label);
    end
    
    h = pie(counts);
    title(plotTitle, 'FontSize', fontsize)
    lg = legend(labels, 'FontSize', fontsize-2);
    lg.Location = 'northeastoutside';
    set(h(2:2:end),'FontSize', fontsize);
    
end

end

