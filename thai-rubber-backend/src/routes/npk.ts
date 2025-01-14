import { Router, Request, Response } from "express";

const router: Router = Router();

router.post("/v1/soil/post", (req, res) => {
    console.log(req.body)
    res.send(`recive\n${JSON.stringify(req.body)}`)
})

export default router