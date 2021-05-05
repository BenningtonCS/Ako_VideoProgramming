Shader "Unlit/Grapes"
{
    Properties
    {
        _Color1 ("Base Color 1", Color) = (1, 1, 1, 1)
        _Wrap("Wrap", Range(0, 1)) = 0
        _ScatterIntensity("Scatter Intensity", Range(0, 1)) = 0
        _ScatterWidth("Scatter Width", Range(0, 1)) = 0
        _ScatterColor("Scatter Color", Color) = (1, 1, 1, 1)
        _Smoothness("Smoothness", Range(0.5, 100)) = 1
        _SpecularIntensity("Specular Intensity", Range(0, 1)) = 1

    }
    SubShader
    {
        Tags {"LightMode" = "ForwardBase"}
        LOD 100

        Pass
        {
            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag
            // make fog work
            #pragma multi_compile_fog
            #pragma multi_compile_fwdbase

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
                UNITY_SHADOW_COORD(1)
                float4 pos : SV_POSITION;
                float4 diffuse : COLOR0;
                float4 ambient : COLOR1; 
                float4 specular : COLOR2;
            };


            float4 _Color1;
            float _Wrap;
            float _ScatterIntensity;
            float _ScatterWidth;
            float4 _ScatterColor;
            float _Smoothness;
            float _SpecularIntensity;

            v2f vert (appdata v)
            {
                v2f o;
                o.pos = UnityObjectToClipPos(v.vertex);
                o.uv = v.uv;
                UNITY_TRANSFER_FOG(o,o.pos);

                float3 normal = UnityObjectToWorldNormal(v.normal);
                float3 vectorToLight = _WorldSpaceLightPos0.xyz; 
                float normalDotLight = dot(normal, vectorToLight);

                float3 reflection = 2 * normalDotLight * normal - vectorToLight;
                fixed3 eye = normalize(UnityWorldSpaceViewDir(mul(unity_ObjectToWorld, v.vertex)));
                float eyeDotR = dot(reflection, eye);

                float wrappedDiffuse = max(0, (normalDotLight + _Wrap) / (1 + _Wrap);
                o.diffuse = wrappedDiffuse * _LightColor0 * (1 - _ScatterIntensity);

                float wrappedEyeDotNormal = max(0, (dot(normal, eye) + _Wrap) / (1 + _Wrap));

                float scatter = smoothstep(0, _ScatterWidth, wrappedEyeDotNormal) * smoothstep(_ScatterWidth * 2, _ScatterWidth, wrappedEyeDotNormal);
                scatter += smoothstep(0, _ScatterWidth, wrappedDiffuse) * smoothstep(_ScatterWidth * 2, _ScatterWidth, wrappedDiffuse);
                
                
                o.diffuse += (scatter * _ScatterColor * _ScatterIntensity);
                o.ambient.rgb = ShadeSH9(float4(normal, 1)) + (_ScatterColor * 0.1);


                o.specular = pow(max(0, eyeDotR), _Smoothness) * _LightColor0;
                TRANSFER_SHADOW(o);

                return o;
            }

            fixed4 frag (v2f i) : SV_Target
            {
                fixed4 col = _Color1 * min(1, (i.diffuse * SHADOW_ATTENUATION(i) + i.ambient));
                // apply fog
                UNITY_APPLY_FOG(i.fogCoord, col);

                return col + (i.specular * _SpecularIntensity);
            }
            ENDCG
        }
        UsePass "LegacyShaders/VertexLit/SHADOWCASTER"
    }
}
