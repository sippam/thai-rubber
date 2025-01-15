import { Router, Request, Response } from "express";

const router: Router = Router();

router.post("/v1/soil/post", (req, res) => {
    console.log(req.body)
    res.status(200).json({ message: "success", data: JSON.stringify(req.body)});
})

export default router