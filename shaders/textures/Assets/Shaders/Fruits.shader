Shader "Unlit/Fruits"
{
    Properties
    {
        _Color1 ("Color1", Color) = (1, 1, 1, 1)
        _Color2 ("Color2", Color) = (0, 0, 0, 0)
        _Periods ("Number of stripes", Range(0,20)) = 1
    }
    SubShader
    {
        //Tags { "RenderType"="Opaque" }
        Tags {"LightMode" = "ForwardBase"}
        LOD 100

        Pass
        {
            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag
            // make fog work
            #pragma multi_compile_fog

            #include "UnityCG.cginc"
            #include "AutoLight.cginc"
            #include "UnityLightingCommon.cginc"

            struct appdata
            {
                float4 vertex : POSITION;
                float2 uv : TEXCOORD0;
                float3 normal: NORMAL;
            };

            struct v2f
            {
                float2 uv : TEXCOORD0;
                UNITY_FOG_COORDS(1)
                float4 vertex : SV_POSITION;
                float4 diffuse : COLOR0;
                float4 specular : COLOR1;
                float4 edges : COLOR2;
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

                float4 worldPos = mul(unity_ObjectToWorld, v.vertex);
                float3 eye = normalize(UnityWorldSpaceViewDir(worldPos));

                float3 worldNormal = UnityObjectToWorldNormal(v.normal);
                float3 lightVector = _WorldSpaceLightPos0.xyz;
                fixed howMuchLight = max(0, dot(worldNormal, lightVector));
                //fixed howMuchLight = 1 - max(0, dot(worldNormal, eye));
                o.diffuse = howMuchLight * fixed4(1, 1, 1, 1);
                o.diffuse.rgb += ShadeSH9(float4(worldNormal, 1));

                float3 projection = dot(worldNormal, lightVector) * worldNormal;
                float3 reflection = 2 * projection - lightVector;

                float howMuchSpecular = max(0, dot(reflection, eye));
                o.specular = pow(howMuchSpecular, 5) * fixed4(1, 1, 1, 1);

                o.edges = (1 - max(0, dot(worldNormal, eye))) * fixed4(1, 1, 1, 1);
                return o;
            
            }

            fixed4 frag (v2f i) : SV_Target
            {

                float sin_stripe = sin(i.uv.y * 2 * 3.1415 * _Periods);
                float cos_stripe = cos(i.uv.x * 2 * 3.1415 * _Periods);

                fixed4 col = lerp(_Color1, _Color2, (sin_stripe + cos_stripe)) * i.diffuse + i.specular * 0.8; //+ i.edges * fixed4(0, 0, 0, 1);

                
                return col;
            }
            ENDCG
        }
    }
}
