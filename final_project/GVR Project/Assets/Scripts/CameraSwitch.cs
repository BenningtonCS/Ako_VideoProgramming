using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CameraSwitch : MonoBehaviour
{
    public GameObject camera1;
    public GameObject camera2;
    public GameObject camera3;

    void Update()
    {
        if(Input.GetButtonDown("RKey"))
        {
            camera1.SetActive(true);
            camera2.SetActive(false);
            camera3.SetActive(false);
        }

        if(Input.GetButtonDown("LKey"))
        {
            camera1.SetActive(false);
            camera2.SetActive(true);
            camera3.SetActive(false);
        }

        if(Input.GetButtonDown("UKey"))
        {
            camera1.SetActive(false);
            camera2.SetActive(false);
            camera3.SetActive(true);
        }
    }
}
