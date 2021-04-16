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
                return frac(sin(x * 2325.23));
            }

            fixed srandom(fixed x)
            {   // random number between -1 and 1
                return random01(x) * 2 - 1;
            }

            fixed4 frag (v2f i) : SV_Target
            {
                fixed2 adj_uv = floor(i.uv * 5);
                //fixed value = sin(i.uv.x * 248992) * 0.5 + 0.5;
                // fixed value = random01(adj_uv.x * 0.1274 + adj_uv.y * -3.14);
                fixed value = abs (srandom(adj_uv.x * -.345 + adj_uv.y * .42));
                return lerp(_Color1, _Color2, clamp(value, 0, 1));
            }
            ENDCG
        }
    }
}
