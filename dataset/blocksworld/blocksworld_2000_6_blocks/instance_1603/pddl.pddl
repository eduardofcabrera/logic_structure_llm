

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(on a d)
(ontable b)
(ontable c)
(ontable d)
(on e a)
(clear b)
(clear c)
(clear e)
)
(:goal
(and
(on a b)
(on b e)
(on d c)
(on e d))
)
)


