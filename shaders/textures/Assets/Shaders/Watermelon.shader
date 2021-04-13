Shader "Unlit/Watermelon"
{
    Properties
    {
        _Color1 ("Color1", Color) = (1, 1, 1, 1)
        _Color2 ("Color2", Color) = (0, 0, 0, 0)
        _Periods ("Number of stripes", Range(0,20)) = 1
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

            fixed4 frag (v2f i) : SV_Target
            {

                float sin_stripe = sin(i.uv.y * 2 * 3.1415 * _Periods);
                float cos_stripe = cos(i.uv.x * 2 * 3.1415 * _Periods);

                fixed4 col = lerp(_Color1, _Color2, (sin_stripe, cos_stripe));

                
                return col;
            }
            ENDCG
        }
    }
}
