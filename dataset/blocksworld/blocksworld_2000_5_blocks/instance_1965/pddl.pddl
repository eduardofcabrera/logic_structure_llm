

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(ontable a)
(on b e)
(ontable c)
(on d a)
(on e d)
(clear b)
(clear c)
)
(:goal
(and
(on a d)
(on c e)
(on d b)
(on e a))
)
)


