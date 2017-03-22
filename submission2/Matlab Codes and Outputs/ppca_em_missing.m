clear;
T1 = imread('eight.tif');
% T1 = rgb2gray(imread('Lenna.png'));

[N, d] = size(T1);

pix_no = 20:10:50;
Error1 = [];
Error2 = [];
for k = 1:length(pix_no)
    T = im2double(T1);

    for n=1:d
        for m=mod(n,2)+1:pix_no(k):N
            T(m,n)=NaN;
        end
    end

    for j = 1:d
        index = mod(j,2)+1:pix_no(k):N;
        temp1 = setdiff(1:N,index);
        temp2 = [];
        for m=1:length(temp1)-1
            temp2 = [temp2 T(temp1(m),j)];
        end
        mu(j) = mean(temp2);
    end

    T2=T;
    for n=1:d
        for m=mod(n,2)+1:pix_no(k):N
            T2(m,n)=mu(n);
        end
    end

    S = zeros(d);
    for n = 1:N
        S = S + (T2(n,:)' - mu') * (T2(n,:)' - mu')';
    end
    S = 1/N * S;        %Covariance matrix
    [d, ~] = size(S);

    %%%%% EM algorithm

    % init
    q = 100;
    W = ones(d, q);
    sigma = 1;
    epsilon = 0.001;

    % loop
    j=1; 
    while (true)
        M = W'*W + sigma^2 * eye(q);
        W_new = S*W*inv(sigma^2 * eye(q) + inv(M)*W'*S*W);
        sigma_new = sqrt(1/d * trace(S - S*W*inv(M)*W_new'));

        if(abs(sigma_new - sigma) < epsilon && max(max(abs(W_new - W))) < epsilon)
            break;
        end

        W = W_new;
        sigma = sigma_new;
        j=j+1;
    end

    W = W_new;
    sigma = sigma_new;

    [N, d] = size(T);
    [~, q] = size(W);

    M = W'*W + sigma^2 * eye(q);

    for i = 1:N
        Tnorm(i,:) = T2(i,:) - mu;
    end

    X = M\W' * Tnorm';

    T_desh = W*X;
    T_desh = T_desh';

    for i=1:N
        T_desh(i,:) = T_desh(i,:) + mu;
    end

    difference = im2double(T1) - im2double(T2);
    squaredError = difference .^ 2;
    meanSquaredError = sum(squaredError(:)) / numel(T1);
    err1 = sqrt(meanSquaredError);

    difference = im2double(T1) - im2double(T_desh);
    squaredError = difference .^ 2;
    meanSquaredError = sum(squaredError(:)) / numel(T1);
    err2 = sqrt(meanSquaredError);
        
    Error1 = [Error1 err1];
    Error2 = [Error2 err2];
end

disp(Error1);
disp(Error2);

figure;
subplot(1,2,1), imshow(T), title('Missing Value Image')
subplot(1,2,2), imshow(T_desh), title('Recovered Image')

% figure;
% plot(pix_no, Error1);hold on;
% xlabel('Miss After x no. of px');
% ylabel('Error');
% 
% plot(pix_no, Error2, '-r');hold on;
% xlabel('Miss After x no. of px');
% ylabel('Error');
% legend('Original-Missing value Input','Original-Retrived');
% title('PPCA with EM (Missing)');