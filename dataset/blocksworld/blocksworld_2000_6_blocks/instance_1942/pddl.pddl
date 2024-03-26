

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(ontable a)
(on b a)
(on c b)
(ontable d)
(on e d)
(clear c)
(clear e)
)
(:goal
(and
(on a b)
(on c a)
(on d e))
)
)


