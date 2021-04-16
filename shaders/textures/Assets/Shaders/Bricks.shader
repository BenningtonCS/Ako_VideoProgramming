Shader "Unlit/Bricks"
{
    Properties
    {
        _Color1 ("Color1", Color) = (1, 1, 1, 1)
        _Color2 ("Color2", Color) = (0, 0, 0, 0)
        _Periods ("Number of stripes", Range(0,200)) = 1
        _Frequency("Frequency", Range(1, 100)) = 4
        _Scale("Scale", Range(0, 10)) = 0.5
    }
    SubShader
    {
        Tags { "RenderType"="Opaque" }
        LOD 100

        Pass
        {
            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag
            // make fog work
            #pragma multi_compile_fog

            #include "UnityCG.cginc"

            struct appdata
            {
                float4 vertex : POSITION;
                float2 uv : TEXCOORD0;
            };

            struct v2f
            {
                float2 uv : TEXCOORD0;
                UNITY_FOG_COORDS(1)
                float4 vertex : SV_POSITION;
            };

            fixed4 _Color1;
            fixed4 _Color2;
            fixed _Periods;
            fixed _Frequency;
            fixed _Scale;

            

            fixed pulse(fixed a, fixed b, fixed x){
                return step(a, x) - step (b, x);
            }

            v2f vert (appdata v)
            {
                v2f o;
                o.vertex = UnityObjectToClipPos(v.vertex);
                o.uv = v.uv;
                UNITY_TRANSFER_FOG(o,o.vertex);

                return o;
            
            }


            fixed random01(fixed x)
            {   // random number between 0 and 1 
                return frac(sin(x * 2321.2));
            }

            fixed srandom(fixed x)
            {   // random number between -1 and 1
                return random01(x) * 2 - 1;
            }

            fixed randomCombo(fixed x, fixed y)
            {   // random combination between x and y 
                return srandom(x * 0.472 + y * y * x * 0.125 + x * x * -0.125);
            }

            fixed2 randomUnitVector(fixed x, fixed y)
            {   // random vector from random combination
                fixed theta = randomCombo(x, y) * 3.1415;
                return fixed2(cos(theta), sin(theta));
            }
            
            fixed dotWithCorner(fixed column, fixed row, fixed2 coordinates)
            {
                fixed2 randomVector = randomUnitVector(column, row);
                fixed2 vectorToPoint = coordinates - fixed2(column, row);
                return dot(randomVector, vectorToPoint);   
            }


            fixed perlinNoise(fixed2 coordinates)
            {   // random number between -1 and 1 for every pixel
                fixed column = floor(coordinates.x);
                fixed row = floor(coordinates.y);

                fixed dot_upperleft = dotWithCorner(column, row, coordinates);
                fixed dot_upperright = dotWithCorner(column + 1, row, coordinates);

                fixed dot_lowerleft = dotWithCorner(column, row + 1, coordinates);
                fixed dot_lowerright = dotWithCorner(column + 1, row + 1, coordinates);


                fixed upper_edge = lerp(dot_upperleft, dot_upperright, smoothstep(0.1, 0.9, frac(coordinates.x)));
                fixed lower_edge = lerp(dot_lowerleft, dot_lowerright, smoothstep(0.1, 0.9, frac(coordinates.x)));

                return lerp(upper_edge, lower_edge, smoothstep(0.1, 0.9, frac(coordinates.y)));
            }

            fixed fractalSum(fixed2 coordinates, fixed minimum_f, fixed maximum_f, fixed stepSize)
            {
                fixed value = 0;
                for (fixed f = minimum_f; f < maximum_f; f *= stepSize) 
                {
                    value += perlinNoise(coordinates * f) /f;
                }
                return value; 
            }

            fixed turbulence(fixed2 coordinates, fixed minimum_f, fixed maximum_f, fixed stepSize)
            {
                fixed value = 0;
                for (fixed f = minimum_f; f < maximum_f; f *= stepSize) 
                {
                    value += abs(perlinNoise(coordinates * f)) /f * 1.5;
                }
                return value; 
            }

            fixed step_hor_stripe_lines(fixed x, fixed y)
            {
                float step_stripe = step(0.4, frac(y * _Periods));
                float hor_line = step(0.4, frac(x * _Periods));
                return step_stripe + hor_line;;
            }

            fixed4 frag (v2f i) : SV_Target
            {

                //float step_stripe = step(0.4, frac(i.uv.y * _Periods));
                //float hor_line = step(0.4, frac(i.uv.x * _Periods));

                //fixed4 col = lerp(_Color1, _Color2, (step_stripe + hor_line));
                fixed x = i.uv.x + turbulence(i.uv.x * _Frequency, 4, 5, 6) * _Scale;
                fixed y = i.uv.y + turbulence(i.uv.y * _Frequency, 4, 5, 6) * _Scale;
                fixed squares = step_hor_stripe_lines(x, y);
                return lerp(_Color1, _Color2, step(0, squares)); 
            }
            ENDCG
        }
    }
}
