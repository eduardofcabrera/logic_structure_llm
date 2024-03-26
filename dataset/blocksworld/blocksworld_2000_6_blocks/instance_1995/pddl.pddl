

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(ontable a)
(on b a)
(on c e)
(ontable d)
(on e d)
(clear b)
(clear c)
)
(:goal
(and
(on b e)
(on d b)
(on e a))
)
)


