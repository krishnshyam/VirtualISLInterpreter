using RogoDigital.Lipsync;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.Xml;

public class play : MonoBehaviour
{
    [SerializeField]
    public AudioClip audioCLip; //leave it none
    public LipSync avatar1;     //3d model 
    public LipSyncData clip1;    //.asset           

    public string filePath;       //folder in resources where all the .xml files are stored 
    public TextAsset targetFile;  //to access xml file 
   
    public Animator anim;           //animator 
    public string animName;         //word to be triggered




    private void Awake()
    {
        Animator anim = FindObjectOfType<Animator>();
    }


    public void Update()
    {
        if (Input.GetKeyDown(KeyCode.Q))
        {
           
            PlayWord(animName);                             
           

        }

    }
    /* this function will trigger animation in 3d model's animator and trigger lipSync data for facial animation*/
    public void PlayWord(string word)
    {
        filePath = "letsgo/" + word;
        targetFile = Resources.Load<TextAsset>(filePath);
       
        // avatar1.Play(clip1);                            // void RogoDigital.Lipsync.LipSync.Play(LipSyncData dataFile)	

        avatar1.Play(targetFile, audioCLip);             // void RogoDigital.Lipsync.LipSync.Play(TextAsset xmlFile, AudioClip clip)
        anim.Play(word);                             //animator.play("word");
    }


    



}
