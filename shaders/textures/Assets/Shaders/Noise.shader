Shader "Unlit/Noise"
{
    Properties
    {
        _Color1 ("Color 1", Color) = (1, 1, 1, 1)
        _Color2 ("Color 2", Color) = (0, 0, 0, 1)
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

            fixed4 frag (v2f i) : SV_Target
            {
                //fixed2 adj_uv = floor(i.uv * 2);
                //fixed value = sin(i.uv.x * 248992) * 0.5 + 0.5;
                //fixed value = random01(adj_uv.x * 0.1274 + adj_uv.y * -3.14);
                fixed value = perlinNoise(i.uv * 10) * 0.4 + 0.3;
                //return fixed4(value.x * 0.5 + 0.5, value.y * 0.5 + 0.5, 0, 1);
                return lerp(_Color1, _Color2, clamp(value, 0, 1));
            }
            ENDCG
        }
    }
}
