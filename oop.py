image_file = "C:\image\testimg.jpg";
img = imread(image_file);

if size (img, 3)
    == 3 img = rgb2gray(img);
end

    counts = histcounts(img( :), 256, 'BinLimits', [ 0, 255 ]);
probabilities = counts / numel(img);
entropy_manual = -sum(probabilities(probabilities > 0).*log2(probabilities(probabilities > 0)));
fprintf('Ентропія: %.4f біти\n', entropy_manual);

img_discrete_2 = floor(double(img) / 2) * 2;
img_discrete_4 = floor(double(img) / 4) * 4;

figure;
imshow(uint8(img_discrete_2));
title('Дискретизоване зображення (крок 2)');

figure;
imshow(uint8(img_discrete_4));
title('Дискретизоване зображення (крок 4)');

levels = [ 8, 16, 64 ];
entropy_quantized = zeros(1, length(levels));

for
    i = 1 : length(levels)
                num_levels = levels(i);
img_quantized = floor(double(img) / (256 / num_levels)) * (256 / num_levels);
img_quantized(img_quantized > 255) = 255;

counts_quantized = histcounts(img_quantized( :), 256, 'BinLimits', [ 0, 255 ]);
probabilities_quantized = counts_quantized / numel(img_quantized);
entropy_quantized(i) = -sum(probabilities_quantized(probabilities_quantized > 0).*log2(probabilities_quantized(probabilities_quantized > 0)));

fprintf('Ентропія (квантування на %d рівнів): %.4f біти\n', num_levels, entropy_quantized(i));
end

    counts_discrete_2 = histcounts(img_discrete_2( :), 256, 'BinLimits', [ 0, 255 ]);
probabilities_discrete_2 = counts_discrete_2 / numel(img_discrete_2);
entropy_discrete_2 = -sum(probabilities_discrete_2(probabilities_discrete_2 > 0).*log2(probabilities_discrete_2(probabilities_discrete_2 > 0)));

counts_discrete_4 = histcounts(img_discrete_4( :), 256, 'BinLimits', [ 0, 255 ]);
probabilities_discrete_4 = counts_discrete_4 / numel(img_discrete_4);
entropy_discrete_4 = -sum(probabilities_discrete_4(probabilities_discrete_4 > 0).*log2(probabilities_discrete_4(probabilities_discrete_4 > 0)));

fprintf('Ентропія (дискретизація з кроком 2): %.4f біти\n', entropy_discrete_2);
fprintf('Ентропія (дискретизація з кроком 4): %.4f біти\n', entropy_discrete_4);

scale_factors = [ 2, 4 ];
restored_images = cell(1, length(scale_factors));

for
    i = 1 : length(scale_factors)
                restored_images{i} = imresize(uint8(img_discrete_2), scale_factors(i), 'nearest');
figure;
imshow(restored_images{i});
title([ 'Відновлене зображення (найближчий сусід), крок ', num2str(scale_factors(i)) ]);
end

for i = 1:length(scale_factors)
    restored_bilinear = imresize(uint8(img_discrete_2), scale_factors(i), 'bilinear');
figure;
imshow(restored_bilinear);
title([ 'Відновлене зображення (білінійна), крок ', num2str(scale_factors(i)) ]);

restored_bicubic = imresize(uint8(img_discrete_2), scale_factors(i), 'bicubic');
figure;
imshow(restored_bicubic);
title([ 'Відновлене зображення (бікубічна), крок ', num2str(scale_factors(i)) ]);
end

    relative_entropy_discrete_2 = entropy_manual - entropy_discrete_2;
relative_entropy_discrete_4 = entropy_manual - entropy_discrete_4;

fprintf('Відносна ентропія (дискретизація, крок 2): %.4f біти\n', relative_entropy_discrete_2);
fprintf('Відносна ентропія (дискретизація, крок 4): %.4f біти\n', relative_entropy_discrete_4);

for
    i = 1 : length(scale_factors)
                entropy_restored_nearest = -sum(histcounts(uint8(restored_images{i}( :)), 256, 'BinLimits', [ 0, 255 ]) / numel(restored_images{i}).*log2(histcounts(uint8(restored_images{i}( :)), 256, 'BinLimits', [ 0, 255 ]) / numel(restored_images{i}) + eps));
relative_entropy_nearest = entropy_manual - entropy_restored_nearest;

fprintf('Відносна ентропія (найближчий сусід), крок %d: %.4f біти\n', scale_factors(i), relative_entropy_nearest);

entropy_restored_bilinear = -sum(histcounts(uint8(imresize(img_discrete_2, scale_factors(i), 'bilinear')( :)), 256, 'BinLimits', [ 0, 255 ]) / numel(restored_bilinear).*log2(histcounts(uint8(imresize(img_discrete_2, scale_factors(i), 'bilinear')( :)), 256, 'BinLimits', [ 0, 255 ]) / numel(restored_bilinear) + eps));
relative_entropy_bilinear = entropy_manual - entropy_restored_bilinear;

fprintf('Відносна ентропія (білінійна), крок %d: %.4f біти\n', scale_factors(i), relative_entropy_bilinear);

entropy_restored_bicubic = -sum(histcounts(uint8(imresize(img_discrete_2, scale_factors(i), 'bicubic')( :)), 256, 'BinLimits', [ 0, 255 ]) / numel(restored_bicubic).*log2(histcounts(uint8(imresize(img_discrete_2, scale_factors(i), 'bicubic')( :)), 256, 'BinLimits', [ 0, 255 ]) / numel(restored_bicubic) + eps));
relative_entropy_bicubic = entropy_manual - entropy_restored_bicubic;

fprintf('Відносна ентропія (бікубічна), крок %d: %.4f біти\n', scale_factors(i), relative_entropy_bicubic);
end
