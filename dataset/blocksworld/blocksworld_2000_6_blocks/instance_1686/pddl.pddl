

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(ontable a)
(on b d)
(on c b)
(on d e)
(ontable e)
(clear a)
(clear c)
)
(:goal
(and
(on a b)
(on b d)
(on c a)
(on d e))
)
)


