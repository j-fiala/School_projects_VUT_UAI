classdef JF_VSC1_regrese < matlab.apps.AppBase

    % Properties that correspond to app components
    properties (Access = public)
        UIFigure                       matlab.ui.Figure
        Hidden_layers                  matlab.ui.control.NumericEditField
        NumberofgeneratedpintsLabel_2  matlab.ui.control.Label
        Number_of_points               matlab.ui.control.NumericEditField
        NumberofgeneratedpintsLabel    matlab.ui.control.Label
        ApproximationofeggholderfunctionusingneuralnetworkLabel  matlab.ui.control.Label
        STARTButton                    matlab.ui.control.Button
        Functionsurfright              matlab.ui.control.UIAxes
        Functionsurfleft               matlab.ui.control.UIAxes
    end

  

    % Callbacks that handle component events
    methods (Access = private)

        % Callback function: Functionsurfleft, Functionsurfright,
        % STARTButton
        function STARTButtonPushed(app, event)
            %Eggholder function
            eggholder = @(x,y) -(y + 47) .* sin(sqrt(abs(x./2 + (y+47)))) - x .* sin(sqrt(abs(x - (y+47))));
            
            % generation of random points
            num_points = app.Number_of_points.Value;
            x = 512 * rand(1, num_points) - 256; 
            y = 512 * rand(1, num_points) - 256; 
            sigma = 10; % deviation of the noise
            z = eggholder(x, y)+ sigma * randn(1);
                              
            % Training a neural network
            inputs = [x; y]; 
            targets = z; 
            hidden_layer_size = app.Hidden_layers.Value;
            net = feedforwardnet(hidden_layer_size);
            net = train(net, inputs, targets);
                        
            % Generating grid points
            [X, Y] = meshgrid(-256:4:256, -256:4:256);
            Z_approx = net([X(:)'; Y(:)']);
            Z_approx = reshape(Z_approx, size(X));
            
            % Plotting solution
            surf(app.Functionsurfleft, X, Y, eggholder(X, Y));
            grid(app.Functionsurfleft,"on")
            scatter3(app.Functionsurfright,x, y, z, 10, z, 'filled');
            grid(app.Functionsurfright,"on")
            hold(app.Functionsurfright,"on")
            surf(app.Functionsurfright, X, Y, Z_approx);
            hold(app.Functionsurfleft,"off")
            hold(app.Functionsurfright,"off")
            
        end

        % Callback function
        function UIAxesButtonDown(app, event)
            
        end

        % Value changed function: Number_of_points
        function Number_of_pointsValueChanged(app, event)
            value = app.Number_of_points.Value;
            
        end

        % Value changed function: Hidden_layers
        function Hidden_layersValueChanged(app, event)
            value = app.Hidden_layers.Value;
            
        end
    end

    % Component initialization
    methods (Access = private)

        % Create UIFigure and components
        function createComponents(app)

            % Create UIFigure and hide until all components are created
            app.UIFigure = uifigure('Visible', 'off');
            app.UIFigure.Color = [0.7294 0.8902 0.5608];
            app.UIFigure.Position = [100 100 948 618];
            app.UIFigure.Name = 'MATLAB App';
            app.UIFigure.Pointer = 'hand';

            % Create Functionsurfleft
            app.Functionsurfleft = uiaxes(app.UIFigure);
            title(app.Functionsurfleft, 'Original function')
            xlabel(app.Functionsurfleft, 'X')
            ylabel(app.Functionsurfleft, 'Y')
            zlabel(app.Functionsurfleft, 'Z')
            app.Functionsurfleft.Color = 'none';
            app.Functionsurfleft.ButtonDownFcn = createCallbackFcn(app, @STARTButtonPushed, true);
            app.Functionsurfleft.Position = [33 216 421 317];

            % Create Functionsurfright
            app.Functionsurfright = uiaxes(app.UIFigure);
            title(app.Functionsurfright, 'Neural network approximation')
            xlabel(app.Functionsurfright, 'X')
            ylabel(app.Functionsurfright, 'Y')
            zlabel(app.Functionsurfright, 'Z')
            app.Functionsurfright.Color = 'none';
            app.Functionsurfright.ButtonDownFcn = createCallbackFcn(app, @STARTButtonPushed, true);
            app.Functionsurfright.Position = [482 224 413 309];

            % Create STARTButton
            app.STARTButton = uibutton(app.UIFigure, 'push');
            app.STARTButton.ButtonPushedFcn = createCallbackFcn(app, @STARTButtonPushed, true);
            app.STARTButton.Position = [544 98 116 45];
            app.STARTButton.Text = 'START';

            % Create ApproximationofeggholderfunctionusingneuralnetworkLabel
            app.ApproximationofeggholderfunctionusingneuralnetworkLabel = uilabel(app.UIFigure);
            app.ApproximationofeggholderfunctionusingneuralnetworkLabel.BackgroundColor = [0.4667 0.6745 0.1882];
            app.ApproximationofeggholderfunctionusingneuralnetworkLabel.HorizontalAlignment = 'center';
            app.ApproximationofeggholderfunctionusingneuralnetworkLabel.FontSize = 24;
            app.ApproximationofeggholderfunctionusingneuralnetworkLabel.FontWeight = 'bold';
            app.ApproximationofeggholderfunctionusingneuralnetworkLabel.Position = [112 547 726 61];
            app.ApproximationofeggholderfunctionusingneuralnetworkLabel.Text = 'Approximation of eggholder function using neural network';

            % Create NumberofgeneratedpintsLabel
            app.NumberofgeneratedpintsLabel = uilabel(app.UIFigure);
            app.NumberofgeneratedpintsLabel.FontWeight = 'bold';
            app.NumberofgeneratedpintsLabel.Position = [241 98 168 99];
            app.NumberofgeneratedpintsLabel.Text = 'Number of generated points';

            % Create Number_of_points
            app.Number_of_points = uieditfield(app.UIFigure, 'numeric');
            app.Number_of_points.Limits = [100 2000];
            app.Number_of_points.RoundFractionalValues = 'on';
            app.Number_of_points.ValueChangedFcn = createCallbackFcn(app, @Number_of_pointsValueChanged, true);
            app.Number_of_points.HorizontalAlignment = 'center';
            app.Number_of_points.FontWeight = 'bold';
            app.Number_of_points.Position = [415 125 90 45];
            app.Number_of_points.Value = 1000;

            % Create NumberofgeneratedpintsLabel_2
            app.NumberofgeneratedpintsLabel_2 = uilabel(app.UIFigure);
            app.NumberofgeneratedpintsLabel_2.FontWeight = 'bold';
            app.NumberofgeneratedpintsLabel_2.Position = [315 27 168 99];
            app.NumberofgeneratedpintsLabel_2.Text = 'Hidden layers';

            % Create Hidden_layers
            app.Hidden_layers = uieditfield(app.UIFigure, 'numeric');
            app.Hidden_layers.Limits = [10 Inf];
            app.Hidden_layers.RoundFractionalValues = 'on';
            app.Hidden_layers.ValueChangedFcn = createCallbackFcn(app, @Hidden_layersValueChanged, true);
            app.Hidden_layers.HorizontalAlignment = 'center';
            app.Hidden_layers.FontWeight = 'bold';
            app.Hidden_layers.Position = [415 54 90 45];
            app.Hidden_layers.Value = 50;

            % Show the figure after all components are created
            app.UIFigure.Visible = 'on';
        end
    end

    % App creation and deletion
    methods (Access = public)

        % Construct app
        function app = JF_VSC1_regrese

            % Create UIFigure and components
            createComponents(app)

            % Register the app with App Designer
            registerApp(app, app.UIFigure)

            if nargout == 0
                clear app
            end
        end

        % Code that executes before app deletion
        function delete(app)

            % Delete UIFigure when app is deleted
            delete(app.UIFigure)
        end
    end
end