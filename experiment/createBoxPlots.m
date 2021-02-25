function createBoxPlots(var, data, questions)
%UNTITLED2 Summary of this function goes here
%   Detailed explanation goes here  
    
fontsize = 16;
plotTitle = questions{var};

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

col = strcat("Var",num2str(var));
labels = ["All", "Group 1", "Group 2", "Group 3"];

chart1 = data.(col);
chart2 = data{data{:,"Var3"}==labels(2),col};
chart3 = data{data{:,"Var3"}==labels(3),col};
chart4 = data{data{:,"Var3"}==labels(4),col};

C = [chart1' chart2' chart3' chart4'];
grp = [zeros(1,length(chart1)), ones(1,length(chart2)), ...
    2*ones(1,length(chart3)), 3*ones(1,length(chart4))];

boxplot(C, grp)
title(plotTitle, 'FontSize', fontsize)
ylabel("Participant Score")
ylim([0.5 7.5])

ax = gca;
ax.YAxis.FontSize = fontsize;

% Change labels
xTick = 1:4;
set(gca,'xtick',xTick)
set(gca,'xticklabel',labels,'FontSize', fontsize)


end

