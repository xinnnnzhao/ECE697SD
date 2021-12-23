using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.InputSystem;

public class PlayerLocomotion : MonoBehaviour
{
    public float MoveSpeed;
    public InputActionReference MoveAction;
    public InputActionReference HeightAction;

    private Vector2 leftHandValue = Vector2.zero;
    private Vector2 rightHandValue = Vector2.zero;

    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        ReadInput();
        CamForMove();
    }

    private void ReadInput()
    {
        leftHandValue = MoveAction.action?.ReadValue<Vector2>() ?? Vector2.zero;
        rightHandValue = HeightAction.action?.ReadValue<Vector2>() ?? Vector2.zero;
    }

    private void CamForMove()
    {
        transform.Translate((Camera.main.transform.forward * MoveSpeed * leftHandValue.y + Camera.main.transform.right * MoveSpeed * leftHandValue.x) * Time.deltaTime, Space.World);

        transform.Translate(transform.up * MoveSpeed * rightHandValue.y * Time.deltaTime, Space.World);
    }
}
